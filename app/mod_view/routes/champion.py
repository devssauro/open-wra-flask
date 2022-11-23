from collections import Counter

from flask import Blueprint, request
from sqlalchemy import Integer, and_, case, cast, func, or_
from sqlalchemy.sql import label

from app.mod_team.models import Player
from app.mod_tournament.models import Champion
from app.mod_view.models import PicksBansPrioView, SingleView
from app.mod_view.utils import agt_time_diff, filter_pb_data, filter_sv_data, format_agt

bp = Blueprint("champion", __name__, url_prefix="/champion")

role_pick = {
    "baron": SingleView.baron_pick,
    "jungle": SingleView.jungle_pick,
    "mid": SingleView.mid_pick,
    "dragon": SingleView.dragon_pick,
    "sup": SingleView.sup_pick,
}


@bp.get("/role/<string:role>")
def get_champions_by_role(role: str):
    return {
        "champions": [
            c.to_dict()
            for c in Champion.query.outerjoin((SingleView, role_pick[role] == Champion.id))
            .filter(role_pick[role].is_not(None), *filter_sv_data(request))
            .order_by(Champion.name)
        ]
    }


@bp.get("")
def get_champions():
    query = (
        PicksBansPrioView.query.with_entities(Champion.id, Champion.name, PicksBansPrioView.role)
        .distinct()
        .outerjoin((Champion, Champion.id == PicksBansPrioView.pick_id))
        .filter(*filter_pb_data(request, "team"))
        .order_by(Champion.name)
    )

    champions = {}
    for row in query:
        if row.id not in champions.keys():
            champions[row.id] = {"id": row.id, "name": row.name, "roles": []}
        champions[row.id]["roles"].append(row.role)

    return {"champions": [champions[key] for key in champions.keys()]}


@bp.get("/<int:champion_id>/kda")
def get_kda(champion_id: int):
    if "role" not in request.args:
        return {"msg": "Selecione a role a ser analisada"}
    role_kda = {
        "baron": {
            "kills": SingleView.baron_kills,
            "deaths": SingleView.baron_deaths,
            "assists": SingleView.baron_assists,
        },
        "jungle": {
            "kills": SingleView.jungle_kills,
            "deaths": SingleView.jungle_deaths,
            "assists": SingleView.jungle_assists,
        },
        "mid": {
            "kills": SingleView.mid_kills,
            "deaths": SingleView.mid_deaths,
            "assists": SingleView.mid_assists,
        },
        "dragon": {
            "kills": SingleView.dragon_kills,
            "deaths": SingleView.dragon_deaths,
            "assists": SingleView.dragon_assists,
        },
        "sup": {
            "kills": SingleView.sup_kills,
            "deaths": SingleView.sup_deaths,
            "assists": SingleView.sup_assists,
        },
    }
    data = (
        SingleView.query.with_entities(
            func.avg(role_kda[request.args["role"]]["kills"]).label("kills"),
            func.avg(role_kda[request.args["role"]]["deaths"]).label("deaths"),
            func.avg(role_kda[request.args["role"]]["assists"]).label("assists"),
        )
        .filter(role_pick[request.args["role"]] == champion_id)
        .first()
    )
    return {
        "kills": round(data.kills, 1),
        "deaths": round(data.deaths, 1),
        "assists": round(data.assists, 1),
        "total_avg": 0 if data.deaths == 0 else (data.kills + data.assists) / data.deaths,
    }


@bp.get("/<int:champion_id>/side")
def get_side_info(champion_id: int):
    selected_roles = (
        request.args.getlist("role")
        if len(request.args.getlist("role")) > 0
        else ["baron", "jungle", "mid", "dragon", "sup"]
    )
    data = (
        SingleView.query.with_entities(
            func.sum(case((SingleView.side == "blue", 1), else_=0)).label("blue_games"),
            func.sum(case((SingleView.side == "red", 1), else_=0)).label("red_games"),
            func.sum(
                case(
                    (and_(SingleView.side == "blue", SingleView.team_id == SingleView.winner), 1),
                    else_=0,
                )
            ).label("blue_wins"),
            func.sum(
                case(
                    (and_(SingleView.side == "red", SingleView.team_id == SingleView.winner), 1),
                    else_=0,
                )
            ).label("red_wins"),
        )
        .filter(
            or_(*[role_pick[role] == champion_id for role in selected_roles]),
            *filter_sv_data(request, "side")
        )
        .first()
    )

    if data.blue_games is None:
        return dict(
            total_games=0,
            blue_games=0,
            red_games=0,
            blue_wins=0,
            red_wins=0,
            total_wins=0,
            percent_total_wins=0,
            percent_total_blue_wins=0,
            percent_total_red_wins=0,
            percent_red_games=0,
            percent_blue_games=0,
        )
    else:
        base = {
            "total_games": data.blue_games + data.red_games,
            "blue_games": data.blue_games,
            "red_games": data.red_games,
            "blue_wins": data.blue_wins,
            "red_wins": data.red_wins,
            "total_wins": data.blue_wins + data.red_wins,
        }
        return {
            **base,
            "percent_total_wins": round((base["total_wins"] / base["total_games"]) * 100, 2),
            "percent_total_blue_wins": 0
            if base["blue_games"] == 0
            else round((base["blue_wins"] / base["blue_games"]) * 100, 2),
            "percent_total_red_wins": 0
            if base["red_games"] == 0
            else round((base["red_wins"] / base["red_games"]) * 100, 2),
            "percent_red_games": 0
            if base["red_games"] == 0
            else round((base["red_games"] / base["total_games"]) * 100, 2),
            "percent_blue_games": 0
            if base["blue_games"] == 0
            else round((base["blue_games"] / base["total_games"]) * 100, 2),
        }


@bp.get("/<int:champion_id>/all_matches")
def get_all_matches(champion_id: int):
    roles = ["baron", "jungle", "mid", "dragon", "sup"]
    selected_roles = (
        request.args.getlist("role") if len(request.args.getlist("role")) > 0 else roles
    )
    maps = [
        sv.map_id
        for sv in SingleView.query.distinct()
        .with_entities(SingleView.map_id)
        .filter(
            or_(*[role_pick[role] == champion_id for role in selected_roles]),
            *filter_sv_data(request)
        )
    ]
    q_with = []
    q_against = []
    for role in roles:
        q_with.append(
            SingleView.query.with_entities(
                Champion.id.label("champion_id"),
                Champion.name.label("champion_name"),
                label("role", role),
                label("team_played", "with"),
                func.count(role_pick[role]).label("qty_match"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
            )
            .outerjoin((Champion, Champion.id == role_pick[role]))
            .filter(
                Champion.id != champion_id,
                or_(*[role_pick[role] == champion_id for role in selected_roles]),
                SingleView.map_id.in_(maps),
            )
            .group_by(Champion.id, Champion.name)
        )
        q_against.append(
            SingleView.query.with_entities(
                Champion.id.label("champion_id"),
                Champion.name.label("champion_name"),
                label("role", role),
                label("team_played", "against"),
                func.count(role_pick[role]).label("qty_match"),
                func.sum(case((SingleView.winner != SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
            )
            .outerjoin((Champion, Champion.id == role_pick[role]))
            .filter(
                and_(*[role_pick[role] != champion_id for role in selected_roles]),
                SingleView.map_id.in_(maps),
            )
            .group_by(Champion.id, Champion.name)
        )

    final_with = q_with[0].union_all(*q_with[1:])
    final_against = q_against[0].union_all(*q_against[1:])

    return {
        "champions_with": [
            {
                "champion_id": d.champion_id,
                "champion_name": d.champion_name,
                "role": d.role,
                "team_played": d.team_played,
                "qty_match": d.qty_match,
                "qty_win": d.qty_win,
            }
            for d in final_with
        ],
        "champions_against": [
            {
                "champion_id": d.champion_id,
                "champion_name": d.champion_name,
                "role": d.role,
                "team_played": d.team_played,
                "qty_match": d.qty_match,
                "qty_win": d.qty_win,
            }
            for d in final_against
        ],
    }


@bp.get("/<int:champion_id>/top3")
def get_top_3(champion_id: int):
    if "role" not in request.args:
        return {"msg": "Selecione a role a ser analisada"}
    roles = ["baron", "jungle", "mid", "dragon", "sup"]
    champions_ids = {c.id: str(c.id) for c in Champion.query.all()}
    champions = {str(c.id): c.to_dict() for c in Champion.query.all()}
    dict_with: dict = {r: [] for r in roles}
    dict_against: dict = {r: [] for r in roles}
    matches = [
        m.map_id
        for m in SingleView.query.with_entities(SingleView.map_id)
        .distinct(SingleView.map_id)
        .filter(role_pick[request.args["role"]] == champion_id)
        .order_by(SingleView.map_id)
    ]
    teams_with = list(
        SingleView.query.filter(
            SingleView.map_id.in_(matches), role_pick[request.args["role"]] == champion_id
        ).order_by(SingleView.id)
    )
    for team in teams_with:
        dict_with["baron"].append(champions_ids[team.baron_pick])
        dict_with["jungle"].append(champions_ids[team.jungle_pick])
        dict_with["mid"].append(champions_ids[team.mid_pick])
        dict_with["dragon"].append(champions_ids[team.dragon_pick])
        dict_with["sup"].append(champions_ids[team.sup_pick])
    teams_against = list(
        SingleView.query.filter(
            SingleView.map_id.in_(matches), role_pick[request.args["role"]] != champion_id
        ).order_by(SingleView.id)
    )
    for team in teams_against:
        dict_against["baron"].append(champions_ids[team.baron_pick])
        dict_against["jungle"].append(champions_ids[team.jungle_pick])
        dict_against["mid"].append(champions_ids[team.mid_pick])
        dict_against["dragon"].append(champions_ids[team.dragon_pick])
        dict_against["sup"].append(champions_ids[team.sup_pick])

    return {
        "teams_with": {
            r: [
                {**champions[c[0]], "frequency": c[1]}
                for c in Counter(dict_with[r]).most_common(3)
            ]
            for r in roles
        },
        "teams_against": {
            r: [
                {**champions[c[0]], "frequency": c[1]}
                for c in Counter(dict_against[r]).most_common(
                    3 if r != request.args["role"] else 100
                )
            ]
            for r in roles
        },
    }


@bp.get("/<int:champion_id>/players")
def get_players_info(champion_id: int):
    selected_roles = (
        request.args.getlist("role")
        if len(request.args.getlist("role")) > 0
        else ["baron", "jungle", "mid", "dragon", "sup"]
    )
    general = (
        PicksBansPrioView.query.with_entities(
            func.round(func.avg(PicksBansPrioView.length_sec), 0).label("avg_length"),
            func.count(PicksBansPrioView.pick_id).label("qty_games"),
            func.sum(cast(PicksBansPrioView.winner, Integer)).label("qty_win"),
            func.round(func.avg(PicksBansPrioView.dmg_taken), 0).label("avg_dmg_taken"),
            func.round(func.avg(PicksBansPrioView.dmg_dealt), 0).label("avg_dmg_dealt"),
            func.round(func.avg(PicksBansPrioView.total_gold), 0).label("avg_total_gold"),
            func.round(
                func.avg(PicksBansPrioView.dmg_taken)
                / (func.avg(PicksBansPrioView.length_sec) / 60),
                0,
            ).label("dtpm"),
            func.round(
                func.avg(PicksBansPrioView.dmg_dealt)
                / (func.avg(PicksBansPrioView.length_sec) / 60),
                0,
            ).label("ddpm"),
            func.round(
                func.avg(PicksBansPrioView.total_gold)
                / (func.avg(PicksBansPrioView.length_sec) / 60),
                0,
            ).label("gpm"),
            func.round(
                case(
                    (func.avg(PicksBansPrioView.total_gold) == 0, 0),
                    else_=func.avg(PicksBansPrioView.dmg_taken)
                    / func.avg(PicksBansPrioView.total_gold),
                ),
                2,
            ).label("dtpg"),
            func.round(
                case(
                    (func.avg(PicksBansPrioView.total_gold) == 0, 0),
                    else_=func.avg(PicksBansPrioView.dmg_dealt)
                    / func.avg(PicksBansPrioView.total_gold),
                ),
                2,
            ).label("ddpg"),
            func.round(func.avg(PicksBansPrioView.kills), 2).label("avg_kills"),
            func.round(func.avg(PicksBansPrioView.deaths), 2).label("avg_deaths"),
            func.round(func.avg(PicksBansPrioView.assists), 2).label("avg_assists"),
            func.round(
                case(
                    (
                        func.avg(PicksBansPrioView.deaths) == 0,
                        func.avg(PicksBansPrioView.kills) + func.avg(PicksBansPrioView.assists),
                    ),
                    else_=(func.avg(PicksBansPrioView.kills) + func.avg(PicksBansPrioView.assists))
                    / func.avg(PicksBansPrioView.deaths),
                ),
                2,
            ).label("avg_kda"),
            cast(func.avg(PicksBansPrioView.length_sec), Integer).label("agt"),
            cast(
                func.avg(
                    case((PicksBansPrioView.winner, PicksBansPrioView.length_sec), else_=None)
                ),
                Integer,
            ).label("agt_win"),
            cast(
                func.avg(
                    case(
                        (PicksBansPrioView.winner.isnot(True), PicksBansPrioView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_loss"),
        )
        .filter(
            *filter_pb_data(request),
            PicksBansPrioView.role.in_(selected_roles),
            PicksBansPrioView.pick_id == champion_id
        )
        .first()
    )
    all_players = (
        PicksBansPrioView.query.with_entities(
            Player.nickname,
            PicksBansPrioView.role.label("role"),
            func.round(func.avg(PicksBansPrioView.length_sec), 0).label("avg_length"),
            func.count(PicksBansPrioView.pick_id).label("qty_games"),
            func.sum(cast(PicksBansPrioView.winner, Integer)).label("qty_win"),
            func.round(func.avg(PicksBansPrioView.dmg_taken), 0).label("avg_dmg_taken"),
            func.round(func.avg(PicksBansPrioView.dmg_dealt), 0).label("avg_dmg_dealt"),
            func.round(func.avg(PicksBansPrioView.total_gold), 0).label("avg_total_gold"),
            func.round(
                func.avg(PicksBansPrioView.dmg_taken)
                / (func.avg(PicksBansPrioView.length_sec) / 60),
                0,
            ).label("dtpm"),
            func.round(
                func.avg(PicksBansPrioView.dmg_dealt)
                / (func.avg(PicksBansPrioView.length_sec) / 60),
                0,
            ).label("ddpm"),
            func.round(
                func.avg(PicksBansPrioView.total_gold)
                / (func.avg(PicksBansPrioView.length_sec) / 60),
                0,
            ).label("gpm"),
            func.round(
                case(
                    (func.avg(PicksBansPrioView.total_gold) == 0, 0),
                    else_=func.avg(PicksBansPrioView.dmg_taken)
                    / func.avg(PicksBansPrioView.total_gold),
                ),
                2,
            ).label("dtpg"),
            func.round(
                case(
                    (func.avg(PicksBansPrioView.total_gold) == 0, 0),
                    else_=func.avg(PicksBansPrioView.dmg_dealt)
                    / func.avg(PicksBansPrioView.total_gold),
                ),
                2,
            ).label("ddpg"),
            func.round(func.avg(PicksBansPrioView.kills), 2).label("avg_kills"),
            func.round(func.avg(PicksBansPrioView.deaths), 2).label("avg_deaths"),
            func.round(func.avg(PicksBansPrioView.assists), 2).label("avg_assists"),
            cast(func.avg(PicksBansPrioView.length_sec), Integer).label("agt"),
            cast(
                func.avg(
                    case((PicksBansPrioView.winner, PicksBansPrioView.length_sec), else_=None)
                ),
                Integer,
            ).label("agt_win"),
            cast(
                func.avg(
                    case(
                        (PicksBansPrioView.winner.isnot(True), PicksBansPrioView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_loss"),
        )
        .outerjoin((Player, Player.id == PicksBansPrioView.player))
        .group_by(Player.nickname, PicksBansPrioView.role)
        .filter(
            *filter_pb_data(request),
            PicksBansPrioView.role.in_(selected_roles),
            PicksBansPrioView.pick_id == champion_id
        )
    )
    return {
        "general": dict(
            avg_length=0,
            qty_games=0,
            qty_win=0,
            avg_dmg_taken=0,
            avg_dmg_dealt=0,
            avg_total_gold=0,
            ddpm=0,
            dtpm=0,
            gpm=0,
            ddpg=0,
            dtpg=0,
            avg_kills=0,
            avg_deaths=0,
            avg_assists=0,
        )
        if general.avg_length is None
        else {
            "avg_length": float(general.avg_length),
            "qty_games": float(general.qty_games),
            "qty_win": float(general.qty_win),
            "avg_dmg_taken": float(general.avg_dmg_taken),
            "avg_dmg_dealt": float(general.avg_dmg_dealt),
            "avg_total_gold": float(general.avg_total_gold),
            "ddpm": float(general.ddpm),
            "dtpm": float(general.dtpm),
            "gpm": float(general.gpm),
            "ddpg": float(general.ddpg),
            "dtpg": float(general.dtpg),
            "avg_kills": float(general.avg_kills),
            "avg_deaths": float(general.avg_deaths),
            "avg_assists": float(general.avg_assists),
            "avg_kda": float(general.avg_kda),
        },
        "players": [
            {
                "nickname": player.nickname,
                "role": player.role,
                "avg_length": float(player.avg_length),
                "qty_games": float(player.qty_games),
                "qty_win": float(player.qty_win),
                "avg_dmg_taken": float(player.avg_dmg_taken),
                "avg_dmg_dealt": float(player.avg_dmg_dealt),
                "avg_total_gold": float(player.avg_total_gold),
                "ddpm": float(player.ddpm),
                "dtpm": float(player.dtpm),
                "gpm": float(player.gpm),
                "ddpg": float(player.ddpg),
                "dtpg": float(player.dtpg),
                "avg_kills": float(player.avg_kills),
                "avg_deaths": float(player.avg_deaths),
                "avg_assists": float(player.avg_assists),
                "avg_kda": round(
                    float(player.avg_kills) + float(player.avg_assists)
                    if int(player.avg_deaths) == 0
                    else (float(player.avg_kills) + float(player.avg_assists))
                    / float(player.avg_deaths),
                    2,
                ),
                "agt": format_agt(player.agt),
                "agt_win": format_agt(player.agt_win or 0),
                "agt_loss": format_agt(player.agt_loss or 0),
                "diff_agt": agt_time_diff(general.agt, player.agt),
                "diff_agt_win": agt_time_diff(general.agt_win, player.agt_win or 0),
                "diff_agt_loss": agt_time_diff(general.agt_loss, player.agt_loss or 0),
            }
            for player in all_players
        ],
    }
