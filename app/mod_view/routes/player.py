from collections import Counter

from flask import Blueprint, request
from sqlalchemy import and_, case, func
from sqlalchemy.sql import label

from app.mod_team.models import Player
from app.mod_tournament.models import Champion
from app.mod_view.models import SingleView
from app.mod_view.utils import filter_sv_data

bp = Blueprint("player", __name__, url_prefix="/player")

role_pick = {
    "baron": SingleView.baron_player,
    "jungle": SingleView.jungle_player,
    "mid": SingleView.mid_player,
    "dragon": SingleView.dragon_player,
    "sup": SingleView.sup_player,
}


@bp.get("/role/<string:role>")
def get_players_by_role(role: str):
    return {
        "players": [
            {"id": c.id, "nickname": c.nickname}
            for c in Player.query.with_entities(Player.id, Player.nickname)
            .distinct()
            .outerjoin((SingleView, role_pick[role] == Player.id))
            .filter(role_pick[role].is_not(None), *filter_sv_data(request))
            .order_by(Player.nickname)
        ]
    }


@bp.get("/<int:player_id>/kda")
def get_kda(player_id: int):
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
        .filter(role_pick[request.args["role"]] == player_id)
        .first()
    )
    return {
        "kills": round(data.kills, 1),
        "deaths": round(data.deaths, 1),
        "assists": round(data.assists, 1),
        "total_avg": 0 if data.deaths == 0 else (data.kills + data.assists) / data.deaths,
    }


@bp.get("/<int:player_id>/side")
def get_side_info(player_id: int):
    if "role" not in request.args:
        return {"msg": "Selecione a role a ser analisada"}
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
        .filter(role_pick[request.args["role"]] == player_id, *filter_sv_data(request, "side"))
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


@bp.get("/<int:player_id>/<int:champion_id>/all_matches")
def get_all_matches(player_id: int, champion_id: int):
    if "role" not in request.args:
        return {"msg": "Selecione a role a ser analisada"}
    if not player_id:
        return {"msg": "Informe o player"}
    if not champion_id:
        return {"msg": "Informe o champion"}

    role_champion_pick = {
        "baron": SingleView.baron_pick,
        "jungle": SingleView.jungle_pick,
        "mid": SingleView.mid_pick,
        "dragon": SingleView.dragon_pick,
        "sup": SingleView.sup_pick,
    }
    roles = ["baron", "jungle", "mid", "dragon", "sup"]
    maps = [
        sv.map_id
        for sv in SingleView.query.with_entities(SingleView.map_id).filter(
            role_pick[request.args["role"]] == player_id,
            role_champion_pick[request.args["role"]] == champion_id,
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
                func.count(role_champion_pick[role]).label("qty_match"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
            )
            .outerjoin((Champion, Champion.id == role_champion_pick[role]))
            .filter(
                Champion.id != champion_id,
                role_champion_pick[request.args["role"]] == champion_id,
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
                func.count(role_champion_pick[role]).label("qty_match"),
                func.sum(case((SingleView.winner != SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
            )
            .outerjoin((Champion, Champion.id == role_champion_pick[role]))
            .filter(
                role_champion_pick[request.args["role"]] != champion_id,
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


@bp.get("/<int:player_id>/top3")
@bp.deprecate("")
def get_top_3(player_id: int):
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
        .filter(role_pick[request.args["role"]] == player_id)
        .order_by(SingleView.map_id)
    ]
    teams_with = list(
        SingleView.query.filter(
            SingleView.map_id.in_(matches), role_pick[request.args["role"]] == player_id
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
            SingleView.map_id.in_(matches), role_pick[request.args["role"]] != player_id
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


@bp.get("/<int:player_id>/champions")
def get_players_info(player_id: int):
    if "role" not in request.args:
        return {"msg": "Selecione a role a ser analisada"}
    role_pick = {
        "baron": {
            "column": SingleView.baron_player,
            "champion": SingleView.baron_pick,
            "columns": [
                func.round(func.avg(SingleView.length_sec), 2).label("avg_length"),
                func.count(SingleView.baron_player).label("qty_games"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
                func.round(func.avg(SingleView.baron_dmg_taken), 2).label("avg_dmg_taken"),
                func.round(func.avg(SingleView.baron_dmg_dealt), 2).label("avg_dmg_dealt"),
                func.round(func.avg(SingleView.baron_total_gold), 2).label("avg_total_gold"),
                func.round(func.avg(SingleView.baron_kills), 2).label("avg_kills"),
                func.round(func.avg(SingleView.baron_deaths), 2).label("avg_deaths"),
                func.round(func.avg(SingleView.baron_assists), 2).label("avg_assists"),
                func.round(
                    func.avg(SingleView.baron_dmg_taken) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("dtpm"),
                func.round(
                    func.avg(SingleView.baron_dmg_dealt) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("ddpm"),
                func.round(
                    func.avg(SingleView.baron_total_gold) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("gpm"),
                case(
                    (func.avg(SingleView.baron_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.baron_dmg_taken)
                        / func.avg(SingleView.baron_total_gold),
                        2,
                    ),
                ).label("dtpg"),
                case(
                    (func.avg(SingleView.baron_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.baron_dmg_dealt)
                        / func.avg(SingleView.baron_total_gold),
                        2,
                    ),
                ).label("ddpg"),
            ],
        },
        "jungle": {
            "column": SingleView.jungle_player,
            "champion": SingleView.jungle_pick,
            "columns": [
                func.round(func.avg(SingleView.length_sec), 2).label("avg_length"),
                func.count(SingleView.jungle_player).label("qty_games"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
                func.round(func.avg(SingleView.jungle_dmg_taken), 2).label("avg_dmg_taken"),
                func.round(func.avg(SingleView.jungle_dmg_dealt), 2).label("avg_dmg_dealt"),
                func.round(func.avg(SingleView.jungle_total_gold), 2).label("avg_total_gold"),
                func.round(func.avg(SingleView.jungle_kills), 2).label("avg_kills"),
                func.round(func.avg(SingleView.jungle_deaths), 2).label("avg_deaths"),
                func.round(func.avg(SingleView.jungle_assists), 2).label("avg_assists"),
                func.round(
                    func.avg(SingleView.jungle_dmg_taken) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("dtpm"),
                func.round(
                    func.avg(SingleView.jungle_dmg_dealt) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("ddpm"),
                func.round(
                    func.avg(SingleView.baron_total_gold) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("gpm"),
                case(
                    (func.avg(SingleView.jungle_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.jungle_dmg_taken)
                        / func.avg(SingleView.jungle_total_gold),
                        2,
                    ),
                ).label("dtpg"),
                case(
                    (func.avg(SingleView.jungle_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.jungle_dmg_dealt)
                        / func.avg(SingleView.jungle_total_gold),
                        2,
                    ),
                ).label("ddpg"),
            ],
        },
        "mid": {
            "column": SingleView.mid_player,
            "champion": SingleView.mid_pick,
            "columns": [
                func.round(func.avg(SingleView.length_sec), 2).label("avg_length"),
                func.count(SingleView.mid_player).label("qty_games"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
                func.round(func.avg(SingleView.mid_dmg_taken), 2).label("avg_dmg_taken"),
                func.round(func.avg(SingleView.mid_dmg_dealt), 2).label("avg_dmg_dealt"),
                func.round(func.avg(SingleView.mid_total_gold), 2).label("avg_total_gold"),
                func.round(func.avg(SingleView.mid_kills), 2).label("avg_kills"),
                func.round(func.avg(SingleView.mid_deaths), 2).label("avg_deaths"),
                func.round(func.avg(SingleView.mid_assists), 2).label("avg_assists"),
                func.round(
                    func.avg(SingleView.mid_dmg_taken) / (func.avg(SingleView.length_sec) / 60), 2
                ).label("dtpm"),
                func.round(
                    func.avg(SingleView.mid_dmg_dealt) / (func.avg(SingleView.length_sec) / 60), 2
                ).label("ddpm"),
                func.round(
                    func.avg(SingleView.mid_total_gold) / (func.avg(SingleView.length_sec) / 60), 2
                ).label("gpm"),
                case(
                    (func.avg(SingleView.mid_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.mid_dmg_taken) / func.avg(SingleView.mid_total_gold), 2
                    ),
                ).label("dtpg"),
                case(
                    (func.avg(SingleView.mid_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.mid_dmg_dealt) / func.avg(SingleView.mid_total_gold), 2
                    ),
                ).label("ddpg"),
            ],
        },
        "dragon": {
            "column": SingleView.dragon_player,
            "champion": SingleView.dragon_pick,
            "columns": [
                func.round(func.avg(SingleView.length_sec), 2).label("avg_length"),
                func.count(SingleView.dragon_player).label("qty_games"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
                func.round(func.avg(SingleView.dragon_dmg_taken), 2).label("avg_dmg_taken"),
                func.round(func.avg(SingleView.dragon_dmg_dealt), 2).label("avg_dmg_dealt"),
                func.round(func.avg(SingleView.dragon_total_gold), 2).label("avg_total_gold"),
                func.round(func.avg(SingleView.dragon_kills), 2).label("avg_kills"),
                func.round(func.avg(SingleView.dragon_deaths), 2).label("avg_deaths"),
                func.round(func.avg(SingleView.dragon_assists), 2).label("avg_assists"),
                func.round(
                    func.avg(SingleView.dragon_dmg_taken) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("dtpm"),
                func.round(
                    func.avg(SingleView.dragon_dmg_dealt) / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("ddpm"),
                func.round(
                    func.avg(SingleView.dragon_total_gold)
                    / (func.avg(SingleView.length_sec) / 60),
                    2,
                ).label("gpm"),
                case(
                    (func.avg(SingleView.dragon_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.dragon_dmg_taken)
                        / func.avg(SingleView.dragon_total_gold),
                        2,
                    ),
                ).label("dtpg"),
                case(
                    (func.avg(SingleView.dragon_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.dragon_dmg_dealt)
                        / func.avg(SingleView.dragon_total_gold),
                        2,
                    ),
                ).label("ddpg"),
            ],
        },
        "sup": {
            "column": SingleView.sup_player,
            "champion": SingleView.sup_pick,
            "columns": [
                func.round(func.avg(SingleView.length_sec), 2).label("avg_length"),
                func.count(SingleView.dragon_player).label("qty_games"),
                func.sum(case((SingleView.winner == SingleView.team_id, 1), else_=0)).label(
                    "qty_win"
                ),
                func.round(func.avg(SingleView.sup_dmg_taken), 2).label("avg_dmg_taken"),
                func.round(func.avg(SingleView.sup_dmg_dealt), 2).label("avg_dmg_dealt"),
                func.round(func.avg(SingleView.sup_total_gold), 2).label("avg_total_gold"),
                func.round(func.avg(SingleView.sup_kills), 2).label("avg_kills"),
                func.round(func.avg(SingleView.sup_deaths), 2).label("avg_deaths"),
                func.round(func.avg(SingleView.sup_assists), 2).label("avg_assists"),
                func.round(
                    func.avg(SingleView.sup_dmg_taken) / (func.avg(SingleView.length_sec) / 60), 2
                ).label("dtpm"),
                func.round(
                    func.avg(SingleView.sup_dmg_dealt) / (func.avg(SingleView.length_sec) / 60), 2
                ).label("ddpm"),
                func.round(
                    func.avg(SingleView.sup_total_gold) / (func.avg(SingleView.length_sec) / 60), 2
                ).label("gpm"),
                case(
                    (func.avg(SingleView.sup_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.sup_dmg_taken) / func.avg(SingleView.sup_total_gold), 2
                    ),
                ).label("dtpg"),
                case(
                    (func.avg(SingleView.sup_total_gold) == 0, 0),
                    else_=func.round(
                        func.avg(SingleView.sup_dmg_dealt) / func.avg(SingleView.sup_total_gold), 2
                    ),
                ).label("ddpg"),
            ],
        },
    }

    general = (
        SingleView.query.with_entities(*role_pick[request.args["role"]]["columns"])
        .filter(role_pick[request.args["role"]]["column"] == player_id, *filter_sv_data(request))
        .first()
    )

    all_champions = (
        SingleView.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("name"),
            *role_pick[request.args["role"]]["columns"]
        )
        .outerjoin(
            (Champion, Champion.id == role_pick[request.args["role"]]["champion"]),
        )
        .filter(role_pick[request.args["role"]]["column"] == player_id, *filter_sv_data(request))
        .group_by(Champion.id, Champion.name)
    )

    return {
        "general": {
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
        },
        "champions": [
            {
                "champion_id": champion.champion_id,
                "name": champion.name,
                "avg_length": float(champion.avg_length),
                "qty_games": float(champion.qty_games),
                "qty_win": float(champion.qty_win),
                "avg_dmg_taken": float(champion.avg_dmg_taken),
                "avg_dmg_dealt": float(champion.avg_dmg_dealt),
                "avg_total_gold": float(champion.avg_total_gold),
                "ddpm": float(champion.ddpm),
                "dtpm": float(champion.dtpm),
                "gpm": float(champion.gpm),
                "ddpg": float(champion.ddpg),
                "dtpg": float(champion.dtpg),
                "avg_kills": float(champion.avg_kills),
                "avg_deaths": float(champion.avg_deaths),
                "avg_assists": float(champion.avg_assists),
            }
            for champion in all_champions
        ],
    }
