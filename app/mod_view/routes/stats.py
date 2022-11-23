from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy import Integer, and_, case, cast, func

from app.mod_team.models import Player, Team
from app.mod_tournament.models import Champion, MatchupMap
from app.mod_view.models import PicksBansPrioView, SingleView
from app.mod_view.utils import agt_time_diff, filter_pb_data, filter_sv_data

bp = Blueprint("stats", __name__, url_prefix="/stats")


@bp.get("/team")
def get_team_stats():
    query = list(
        SingleView.query.with_entities(
            Team.id.label("team_id"),
            Team.name.label("team_name"),
            Team.tag.label("team_tag"),
            func.count(SingleView.team_id).label("qty_games"),
            func.sum(cast(SingleView.winner == SingleView.team_id, Integer)).label("qty_win"),
            func.sum(case((SingleView.side == "blue", 1), else_=0)).label("qty_blue"),
            func.sum(case((SingleView.side == "red", 1), else_=0)).label("qty_red"),
            func.sum(
                case(
                    (and_(SingleView.side == "blue", SingleView.winner_side == "blue"), 1), else_=0
                )
            ).label("win_blue"),
            func.sum(
                case((and_(SingleView.side == "red", SingleView.winner_side == "red"), 1), else_=0)
            ).label("win_red"),
            cast(func.avg(SingleView.length_sec), Integer).label("agt"),
            cast(
                func.avg(
                    case(
                        (SingleView.side == SingleView.winner_side, SingleView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_win"),
            cast(
                func.avg(
                    case(
                        (SingleView.side != SingleView.winner_side, SingleView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_loss"),
        )
        .filter(*filter_sv_data(request, "side"))
        .outerjoin((Team, Team.id == SingleView.team_id))
        .group_by(Team.id, Team.name, Team.tag)
    )
    agt = int(sum([t.agt for t in query]) / len(query))
    return {
        "teams": [
            {
                "team_id": team.team_id,
                "team_name": team.team_name,
                "team_tag": team.team_tag,
                "qty_games": team.qty_games,
                "qty_win": team.qty_win,
                "wr": round((team.qty_win / team.qty_games) * 100, 2),
                "qty_blue_games": team.qty_blue,
                "win_blue_games": team.qty_win,
                "wr_blue": "-"
                if team.qty_blue == 0
                else round((team.win_blue / team.qty_blue) * 100, 2),
                "qty_red_games": team.qty_red,
                "win_red_games": team.qty_win,
                "wr_red": "-"
                if team.qty_red == 0
                else round((team.win_red / team.qty_red) * 100, 2),
                "agt": "{1}:{2}".format(*str(timedelta(seconds=team.agt)).split(":")),
                "agt_win": "-"
                if team.agt_win is None
                else "{1}:{2}".format(*str(timedelta(seconds=team.agt_win or 0)).split(":")),
                "agt_loss": "-"
                if team.agt_loss is None
                else "{1}:{2}".format(*str(timedelta(seconds=team.agt_loss or 0)).split(":")),
                "diff_agt": agt_time_diff(agt, team.agt),
                "diff_agt_win": agt_time_diff(agt, team.agt_win or 0),
                "diff_agt_loss": agt_time_diff(agt, team.agt_loss or 0),
            }
            for team in query
        ]
    }


@bp.get("/champion")
def get_champion_stats():
    champions = list(
        Champion.query.with_entities(
            Champion.id.label("id"),
            Champion.name.label("name"),
        )
        .filter(*filter_pb_data(request))
        .order_by(Champion.name)
        .distinct()
        .outerjoin(
            (
                PicksBansPrioView,
                Champion.id.in_([PicksBansPrioView.pick_id, PicksBansPrioView.ban_id]),
            )
        )
    )
    args = []
    if "patch" in request.args:
        args.append(MatchupMap.patch == request.args["patch"])
    if "t" in request.args:
        args.append(MatchupMap.tournament_id == request.args["t"])
    total_games = (
        MatchupMap.query.with_entities(func.count(MatchupMap.id).label("total"))
        .filter(*args)
        .first()
        .total
    )
    query = list(
        PicksBansPrioView.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("champion_name"),
            func.round(func.avg(PicksBansPrioView.kills), 2).label("avg_kills"),
            func.round(func.avg(PicksBansPrioView.deaths), 2).label("avg_deaths"),
            func.round(func.avg(PicksBansPrioView.assists), 2).label("avg_assists"),
            func.round(
                case(
                    (
                        func.avg(PicksBansPrioView.deaths) > 0,
                        (func.avg(PicksBansPrioView.kills) + func.avg(PicksBansPrioView.assists))
                        / func.avg(PicksBansPrioView.deaths),
                    ),
                    else_=func.avg(PicksBansPrioView.kills) + func.avg(PicksBansPrioView.assists),
                ),
                2,
            ).label("avg_kda"),
            func.round(
                func.avg(PicksBansPrioView.dmg_dealt)
                / (func.avg(PicksBansPrioView.length_sec / 60)),
                0,
            ).label("ddpm"),
            func.round(
                func.avg(PicksBansPrioView.total_gold)
                / (func.avg(PicksBansPrioView.length_sec / 60)),
                0,
            ).label("gpm"),
            func.count(PicksBansPrioView.pick_id).label("qty_picks"),
            func.sum(cast(PicksBansPrioView.winner, Integer)).label("qty_win"),
            func.sum(case((PicksBansPrioView.side == "blue", 1), else_=0)).label("qty_blue"),
            func.sum(case((PicksBansPrioView.side == "red", 1), else_=0)).label("qty_red"),
            func.sum(
                cast(and_(PicksBansPrioView.side == "blue", PicksBansPrioView.winner), Integer)
            ).label("win_blue"),
            func.sum(
                cast(and_(PicksBansPrioView.side == "red", PicksBansPrioView.winner), Integer)
            ).label("win_red"),
            cast(func.avg(PicksBansPrioView.length_sec), Integer).label("agt"),
            cast(
                func.avg(
                    case(
                        (PicksBansPrioView.winner.is_(True), PicksBansPrioView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_win"),
            cast(
                func.avg(
                    case(
                        (PicksBansPrioView.winner.is_(False), PicksBansPrioView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_loss"),
        )
        .filter(*filter_pb_data(request, "side"))
        .outerjoin((Champion, Champion.id == PicksBansPrioView.pick_id))
        .group_by(Champion.id, Champion.name)
        .distinct()
        .order_by(Champion.name)
    )
    agt = int(sum([t.agt for t in query]) / len(query))
    pick_dict = [
        {
            "champion_id": champion.champion_id,
            "champion_name": champion.champion_name,
            "avg_kills": float(champion.avg_kills),
            "avg_deaths": float(champion.avg_deaths),
            "avg_assists": float(champion.avg_assists),
            "ddpm": float(champion.ddpm),
            "gpm": float(champion.gpm),
            "ddpg": round(float(champion.ddpm) / float(champion.gpm), 2),
            "avg_kda": None if champion.avg_kda is None else float(champion.avg_kda),
            "qty_picks": champion.qty_picks,
            "qty_win": champion.qty_win,
            "wr": round((champion.qty_win / champion.qty_picks) * 100, 2),
            "qty_blue_games": champion.qty_blue,
            "win_blue_games": champion.qty_win,
            "wr_blue": "-"
            if champion.qty_blue == 0
            else round((champion.win_blue / champion.qty_blue) * 100, 2),
            "qty_red_games": champion.qty_red,
            "win_red_games": champion.qty_win,
            "wr_red": "-"
            if champion.qty_red == 0
            else round((champion.win_red / champion.qty_red) * 100, 2),
            "agt": "{1}:{2}".format(*str(timedelta(seconds=champion.agt)).split(":")),
            "agt_win": "-"
            if champion.agt_win is None
            else "{1}:{2}".format(*str(timedelta(seconds=champion.agt_win or 0)).split(":")),
            "agt_loss": "-"
            if champion.agt_loss is None
            else "{1}:{2}".format(*str(timedelta(seconds=champion.agt_loss or 0)).split(":")),
            "diff_agt": agt_time_diff(agt, champion.agt),
            "diff_agt_win": agt_time_diff(agt, champion.agt_win or 0),
            "diff_agt_loss": agt_time_diff(agt, champion.agt_loss or 0),
        }
        for champion in query
    ]
    ban_dict = [
        {"champion_id": row.champion_id, "qty_bans": row.qty_bans}
        for row in Champion.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("champion_name"),
            func.count(PicksBansPrioView.pick_id).label("qty_bans"),
        )
        .filter(*filter_pb_data(request, "side"))
        .outerjoin((Champion, Champion.id == PicksBansPrioView.ban_id))
        .group_by(Champion.id, Champion.name)
        .distinct()
        .order_by(Champion.name)
    ]
    data = []
    for c in champions:
        pick_presence = [row for row in pick_dict if row["champion_id"] == c.id]
        ban_presence = [row for row in ban_dict if row["champion_id"] == c.id]
        if len(pick_presence) > 0 or len(ban_presence):
            qty_picks = 0 if len(pick_presence) == 0 else pick_presence[0]["qty_picks"]
            qty_bans = 0 if len(ban_presence) == 0 else ban_presence[0]["qty_bans"]
            qty_presence = qty_picks + qty_bans
            if len(pick_presence) > 0:
                data.append(
                    {
                        **pick_presence[0],
                        "qty_presence": qty_presence,
                        "percent_presence": "-"
                        if qty_presence == 0
                        else round((qty_presence / total_games) * 100, 2),
                        "qty_bans": qty_bans,
                    }
                )
    return {"champions": data}


@bp.get("/player")
def get_player_stats():
    # args = []
    # if 'patch' in request.args:
    #     args.append(MatchupMap.patch == request.args['patch'])
    # if 't' in request.args:
    #     args.append(MatchupMap.tournament_id == request.args['t'])
    # total_games = MatchupMap.query.with_entities(
    #     func.count(MatchupMap.id).label('total')).filter(*args).first().total
    query = list(
        PicksBansPrioView.query.with_entities(
            Player.id.label("id"),
            Player.nickname.label("nickname"),
            PicksBansPrioView.role,
            func.round(func.avg(PicksBansPrioView.kills), 2).label("avg_kills"),
            func.round(func.avg(PicksBansPrioView.deaths), 2).label("avg_deaths"),
            func.round(func.avg(PicksBansPrioView.assists), 2).label("avg_assists"),
            func.round(
                case(
                    (
                        func.avg(PicksBansPrioView.deaths) > 0,
                        (func.avg(PicksBansPrioView.kills) + func.avg(PicksBansPrioView.assists))
                        / func.avg(PicksBansPrioView.deaths),
                    ),
                    else_=func.avg(PicksBansPrioView.kills) + func.avg(PicksBansPrioView.assists),
                ),
                2,
            ).label("avg_kda"),
            func.round(
                func.avg(PicksBansPrioView.dmg_dealt)
                / (func.avg(PicksBansPrioView.length_sec / 60)),
                0,
            ).label("ddpm"),
            func.round(
                func.avg(PicksBansPrioView.total_gold)
                / (func.avg(PicksBansPrioView.length_sec / 60)),
                0,
            ).label("gpm"),
            func.count(PicksBansPrioView.player).label("qty_games"),
            func.sum(cast(PicksBansPrioView.winner, Integer)).label("qty_win"),
            func.sum(case((PicksBansPrioView.side == "blue", 1), else_=0)).label("qty_blue"),
            func.sum(case((PicksBansPrioView.side == "red", 1), else_=0)).label("qty_red"),
            func.sum(
                cast(and_(PicksBansPrioView.side == "blue", PicksBansPrioView.winner), Integer)
            ).label("win_blue"),
            func.sum(
                cast(and_(PicksBansPrioView.side == "red", PicksBansPrioView.winner), Integer)
            ).label("win_red"),
            cast(func.avg(PicksBansPrioView.length_sec), Integer).label("agt"),
            cast(
                func.avg(
                    case(
                        (PicksBansPrioView.winner.is_(True), PicksBansPrioView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_win"),
            cast(
                func.avg(
                    case(
                        (PicksBansPrioView.winner.is_(False), PicksBansPrioView.length_sec),
                        else_=None,
                    )
                ),
                Integer,
            ).label("agt_loss"),
        )
        .filter(*filter_pb_data(request, "side"))
        .outerjoin((Player, Player.id == PicksBansPrioView.player))
        .group_by(Player.id, PicksBansPrioView.role, Player.nickname)
        .order_by(Player.nickname)
    )
    agt = int(sum([t.agt for t in query]) / len(query))
    return {
        "players": [
            {
                "player_id": player.id,
                "nickname": player.nickname,
                "role": player.role,
                "avg_kills": float(player.avg_kills),
                "avg_deaths": float(player.avg_deaths),
                "avg_assists": float(player.avg_assists),
                "ddpm": float(player.ddpm),
                "gpm": float(player.gpm),
                "ddpg": round(float(player.ddpm) / float(player.gpm), 2),
                "avg_kda": None if player.avg_kda is None else float(player.avg_kda),
                "qty_picks": player.qty_games,
                "qty_win": player.qty_win,
                "wr": round((player.qty_win / player.qty_games) * 100, 2),
                "qty_blue_games": player.qty_blue,
                "win_blue_games": player.qty_win,
                "wr_blue": "-"
                if player.qty_blue == 0
                else round((player.win_blue / player.qty_blue) * 100, 2),
                "qty_red_games": player.qty_red,
                "win_red_games": player.qty_win,
                "wr_red": "-"
                if player.qty_red == 0
                else round((player.win_red / player.qty_red) * 100, 2),
                "agt": "{1}:{2}".format(*str(timedelta(seconds=player.agt)).split(":")),
                "agt_win": "-"
                if player.agt_win is None
                else "{1}:{2}".format(*str(timedelta(seconds=player.agt_win or 0)).split(":")),
                "agt_loss": "-"
                if player.agt_loss is None
                else "{1}:{2}".format(*str(timedelta(seconds=player.agt_loss or 0)).split(":")),
                "diff_agt": agt_time_diff(agt, player.agt),
                "diff_agt_win": agt_time_diff(agt, player.agt_win or 0),
                "diff_agt_loss": agt_time_diff(agt, player.agt_loss or 0),
            }
            for player in query
        ]
    }
