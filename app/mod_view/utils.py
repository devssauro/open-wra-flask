from datetime import timedelta

from flask import Request
from sqlalchemy import and_, or_
from sqlalchemy.sql.elements import BinaryExpression

from app.mod_tournament.models import MatchupMap
from app.mod_view.models import ObjectiveView, PicksBansPrioView, SingleView


def filter_by_id(column, val):
    return column.in_(val) if type(val) in (list, tuple) else column == val


def team_expression_resolver(team_type: str, team_id: int) -> BinaryExpression:
    if team_type == "taker":
        return and_(ObjectiveView.team_id == team_id, ObjectiveView.team_id.isnot(None))
    if team_type == "giver":
        return and_(
            ObjectiveView.team_giver_id == team_id, ObjectiveView.team_giver_id.isnot(None)
        )
    if team_type == "-":
        return ObjectiveView.team_id.is_(None)


def filter_sv_data(request: Request, ignore: str = None):
    args = []
    if ignore != "side" and "side" in request.args and request.args["side"] in ("blue", "red"):
        args.append(SingleView.side == request.args["side"])
    if ignore != "t" and "t" in request.args:
        _t = [int(t) for t in request.args.getlist("t")]
        args.append(SingleView.tournament_id.in_(_t))
    if ignore != "patch" and "patch" in request.args:
        args.append(SingleView.patch.in_(request.args.getlist("patch")))
    if ignore != "team" and "team" in request.args:
        _teams = [int(t) for t in request.args.getlist("team")]
        args.append(SingleView.team_id.in_(_teams))
    return args


def filter_map_data(request: Request, ignore: str = None):
    args = []
    # if ignore != 'side' and 'side' in request.args and request.args['side'] in ('blue', 'red'):
    #     args.append(MatchupMap.side == request.args['side'])
    if ignore != "t" and "t" in request.args:
        _t = [int(t) for t in request.args.getlist("t")]
        args.append(MatchupMap.tournament_id.in_(_t))
    if ignore != "patch" and "patch" in request.args:
        args.append(MatchupMap.patch.in_(request.args.getlist("patch")))
    if ignore != "team" and "team" in request.args:
        _teams = [int(t) for t in request.args.getlist("team")]
        args.append(or_(MatchupMap.blue_side.in_(_teams), MatchupMap.red_side.in_(_teams)))
    return args


def filter_pb_data(request: Request, ignore: str = None):
    args = []
    if ignore != "side" and "side" in request.args and request.args["side"] in ("blue", "red"):
        args.append(PicksBansPrioView.side == request.args["side"])
    if ignore != "t" and "t" in request.args:
        _t = [int(t) for t in request.args.getlist("t")]
        args.append(PicksBansPrioView.tournament_id.in_(_t))
    if ignore != "patch" and "patch" in request.args:
        args.append(PicksBansPrioView.patch.in_(request.args.getlist("patch")))
    if ignore != "team" and "team" in request.args:
        # _t = [int(t) for t in request.args.getlist('team')]
        _teams = [int(t) for t in request.args.getlist("team")]
        args.append(PicksBansPrioView.team_id.in_(_teams))
    return args


def prio_percent(picks: int, games: int, side: str, rotation: int):
    if games == 0:
        return "0.0%"
    if side == "blue" and rotation == 1 or side == "red" and rotation > 1:
        return f"{round((picks / games) * 100, 2)}%"
    else:
        return f"{round((picks / games) * 100, 2)}%"


def prio_percent_wr(picks: int, games: int, side: str, rotation: int, role: str):
    if picks == 0:
        return "-"
    if side == "blue" and rotation == 1 or side == "red" and rotation > 1:
        return f"{round((games / picks) * 100, 2)}%"
    else:
        return f"{round((games / picks) * 100, 2)}%"


def format_agt(agt):
    if agt == 0:
        return "-"
    time = str(timedelta(seconds=agt)).split(":")
    return f"{time[1]}:{time[2][0:2]}"


def agt_time_diff(agt_all, agt_team):
    if agt_all is None:
        return "-"
    if agt_all > agt_team:
        time = str(timedelta(seconds=agt_all - agt_team)).split(":")
        return f"-{time[1]}:{time[2][0:2]}"
    else:
        time = str(timedelta(seconds=agt_team - agt_all)).split(":")
        return f"+{time[1]}:{time[2][0:2]}"
