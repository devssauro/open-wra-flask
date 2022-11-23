from flask import Blueprint, request
from sqlalchemy import Integer, and_, case, func

from app.mod_tournament.models import Champion, MatchupMap
from app.mod_view.models import PicksBansPrioView
from app.mod_view.utils import filter_pb_data, prio_percent, prio_percent_wr

bp = Blueprint("picks", __name__, url_prefix="")


@bp.get("prio")
def get_prio_rotation():
    prio = (
        PicksBansPrioView.query.with_entities(
            PicksBansPrioView.side,
            PicksBansPrioView.pick_rotation,
            PicksBansPrioView.role,
            func.count(PicksBansPrioView.role).label("total"),
            func.sum(case((PicksBansPrioView.winner, 1), else_=0)).label("total_win"),
        )
        .filter(*filter_pb_data(request, "side"))
        .group_by(PicksBansPrioView.side, PicksBansPrioView.pick_rotation, PicksBansPrioView.role)
        .order_by(
            PicksBansPrioView.side,
            PicksBansPrioView.pick_rotation,
            func.count(PicksBansPrioView.role).desc(),
        )
    )

    total_games = {
        "blue": sum([p.total for p in prio if p.side == "blue" and p.pick_rotation == 1]),
        "red": sum([p.total for p in prio if p.side == "red" and p.pick_rotation == 2]),
    }

    prio_role = {"blue": {1: {}, 2: {}, 3: {}}, "red": {1: {}, 2: {}, 3: {}, 4: {}}}
    wr_role = {"blue": {1: {}, 2: {}, 3: {}}, "red": {1: {}, 2: {}, 3: {}, 4: {}}}

    for row in prio:
        prio_role[row.side][row.pick_rotation][row.role] = row.total
        wr_role[row.side][row.pick_rotation][row.role] = row.total_win

    final_list = []
    wr_list = []
    for side in prio_role.keys():
        for rotation in prio_role[side].keys():
            final_list.append(
                {
                    "side": side,
                    "rotation": rotation,
                    "baron": prio_percent(
                        prio_role[side][rotation].get("baron", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "jungle": prio_percent(
                        prio_role[side][rotation].get("jungle", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "mid": prio_percent(
                        prio_role[side][rotation].get("mid", 0), total_games[side], side, rotation
                    ),
                    "dragon": prio_percent(
                        prio_role[side][rotation].get("dragon", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "sup": prio_percent(
                        prio_role[side][rotation].get("sup", 0), total_games[side], side, rotation
                    ),
                }
            )
            wr_list.append(
                {
                    "side": side,
                    "rotation": rotation,
                    "baron": prio_percent_wr(
                        prio_role[side][rotation].get("baron", 0),
                        wr_role[side][rotation].get("baron", 0),
                        side,
                        rotation,
                        "baron",
                    ),
                    "jungle": prio_percent_wr(
                        prio_role[side][rotation].get("jungle", 0),
                        wr_role[side][rotation].get("jungle", 0),
                        side,
                        rotation,
                        "jungle",
                    ),
                    "mid": prio_percent_wr(
                        prio_role[side][rotation].get("mid", 0),
                        wr_role[side][rotation].get("mid", 0),
                        side,
                        rotation,
                        "mid",
                    ),
                    "dragon": prio_percent_wr(
                        prio_role[side][rotation].get("dragon", 0),
                        wr_role[side][rotation].get("dragon", 0),
                        side,
                        rotation,
                        "dragon",
                    ),
                    "sup": prio_percent_wr(
                        prio_role[side][rotation].get("sup", 0),
                        wr_role[side][rotation].get("sup", 0),
                        side,
                        rotation,
                        "sup",
                    ),
                }
            )
    return dict(prio=final_list, prio_wr=wr_list)


@bp.get("blind")
def get_blind_rotation():
    blind_query = (
        PicksBansPrioView.query.with_entities(
            PicksBansPrioView.side.label("side"),
            PicksBansPrioView.pick_rotation.label("pick_rotation"),
            PicksBansPrioView.role.label("role"),
            func.sum(case((PicksBansPrioView.is_blind, 1), else_=0)).label("total_blind"),
            func.sum(
                case((and_(PicksBansPrioView.is_blind, PicksBansPrioView.winner), 1), else_=0)
            ).label("win_blind"),
            func.sum(case((PicksBansPrioView.is_blind, 0), else_=1)).label("total_response"),
            func.sum(
                case(
                    (and_(PicksBansPrioView.is_blind.is_(False), PicksBansPrioView.winner), 1),
                    else_=0,
                )
            ).label("win_response"),
        )
        .filter(*filter_pb_data(request, "side"))
        .group_by(PicksBansPrioView.side, PicksBansPrioView.pick_rotation, PicksBansPrioView.role)
        .order_by(PicksBansPrioView.side, PicksBansPrioView.pick_rotation, PicksBansPrioView.role)
    )

    total_games = {
        "blue": sum(
            [p.total_blind for p in blind_query if p.side == "blue" and p.pick_rotation == 1]
        ),
        "red": sum(
            [p.total_response for p in blind_query if p.side == "red" and p.pick_rotation == 4]
        ),
    }

    blind_role = {
        "blue": {
            "total": {
                "total_blind": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
                "win_blind": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
                "total_response": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
                "win_response": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
            },
            1: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
            2: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
            3: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
        },
        "red": {
            "total": {
                "total_blind": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
                "win_blind": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
                "total_response": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
                "win_response": {"baron": 0, "jungle": 0, "mid": 0, "dragon": 0, "sup": 0},
            },
            1: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
            2: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
            3: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
            4: {"baron": {}, "jungle": {}, "mid": {}, "dragon": {}, "sup": {}},
        },
    }

    for index, row in enumerate(blind_query):
        blind_role[row.side][row.pick_rotation][row.role]["total_blind"] = row.total_blind
        blind_role[row.side][row.pick_rotation][row.role]["win_blind"] = row.win_blind
        blind_role[row.side][row.pick_rotation][row.role]["total_response"] = row.total_response
        blind_role[row.side][row.pick_rotation][row.role]["win_response"] = row.win_response

    blind_list = []
    blind_wr_list = []
    response_list = []
    response_wr_list = []
    for side in blind_role.keys():
        for rotation in [r for r in blind_role[side].keys() if r != "total"]:
            blind_list.append(
                {
                    "side": side,
                    "rotation": rotation,
                    "baron": prio_percent(
                        blind_role[side][rotation]["baron"].get("total_blind", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "jungle": prio_percent(
                        blind_role[side][rotation]["jungle"].get("total_blind", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "mid": prio_percent(
                        blind_role[side][rotation]["mid"].get("total_blind", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "dragon": prio_percent(
                        blind_role[side][rotation]["dragon"].get("total_blind", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "sup": prio_percent(
                        blind_role[side][rotation]["sup"].get("total_blind", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                }
            )
            blind_wr_list.append(
                {
                    "side": side,
                    "rotation": rotation,
                    "baron": prio_percent_wr(
                        blind_role[side][rotation]["baron"].get("total_blind", 0),
                        blind_role[side][rotation]["baron"].get("win_blind", 0),
                        side,
                        rotation,
                        "baron",
                    ),
                    "jungle": prio_percent_wr(
                        blind_role[side][rotation]["jungle"].get("total_blind", 0),
                        blind_role[side][rotation]["jungle"].get("win_blind", 0),
                        side,
                        rotation,
                        "jungle",
                    ),
                    "mid": prio_percent_wr(
                        blind_role[side][rotation]["mid"].get("total_blind", 0),
                        blind_role[side][rotation]["mid"].get("win_blind", 0),
                        side,
                        rotation,
                        "mid",
                    ),
                    "dragon": prio_percent_wr(
                        blind_role[side][rotation]["dragon"].get("total_blind", 0),
                        blind_role[side][rotation]["dragon"].get("win_blind", 0),
                        side,
                        rotation,
                        "dragon",
                    ),
                    "sup": prio_percent_wr(
                        blind_role[side][rotation]["sup"].get("total_blind", 0),
                        blind_role[side][rotation]["sup"].get("win_blind", 0),
                        side,
                        rotation,
                        "sup",
                    ),
                }
            )
            response_list.append(
                {
                    "side": side,
                    "rotation": rotation,
                    "baron": prio_percent(
                        blind_role[side][rotation]["baron"].get("total_response", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "jungle": prio_percent(
                        blind_role[side][rotation]["jungle"].get("total_response", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "mid": prio_percent(
                        blind_role[side][rotation]["mid"].get("total_response", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "dragon": prio_percent(
                        blind_role[side][rotation]["dragon"].get("total_response", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                    "sup": prio_percent(
                        blind_role[side][rotation]["sup"].get("total_response", 0),
                        total_games[side],
                        side,
                        rotation,
                    ),
                }
            )
            response_wr_list.append(
                {
                    "side": side,
                    "rotation": rotation,
                    "baron": prio_percent_wr(
                        blind_role[side][rotation]["baron"].get("total_response", 0),
                        blind_role[side][rotation]["baron"].get("win_response", 0),
                        side,
                        rotation,
                        "baron",
                    ),
                    "jungle": prio_percent_wr(
                        blind_role[side][rotation]["jungle"].get("total_response", 0),
                        blind_role[side][rotation]["jungle"].get("win_response", 0),
                        side,
                        rotation,
                        "jungle",
                    ),
                    "mid": prio_percent_wr(
                        blind_role[side][rotation]["mid"].get("total_response", 0),
                        blind_role[side][rotation]["mid"].get("win_response", 0),
                        side,
                        rotation,
                        "mid",
                    ),
                    "dragon": prio_percent_wr(
                        blind_role[side][rotation]["dragon"].get("total_response", 0),
                        blind_role[side][rotation]["dragon"].get("win_response", 0),
                        side,
                        rotation,
                        "dragon",
                    ),
                    "sup": prio_percent_wr(
                        blind_role[side][rotation]["sup"].get("total_response", 0),
                        blind_role[side][rotation]["sup"].get("win_response", 0),
                        side,
                        rotation,
                        "sup",
                    ),
                }
            )

    return dict(
        blind=blind_list,
        blind_wr=blind_wr_list,
        response=response_list,
        response_wr=response_wr_list,
    )


@bp.get("picks")
def get_pick_rotation():
    data = filter_pb_data(request, "side")
    query = list(
        PicksBansPrioView.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("champion_name"),
            PicksBansPrioView.pick_rotation.label("rotation"),
            func.count(PicksBansPrioView.pick_id).label("qty_picks"),
            PicksBansPrioView.side.label("side"),
            func.sum(case((PicksBansPrioView.winner, 1), else_=0)).label("qty_win"),
        )
        .outerjoin((Champion, Champion.id == PicksBansPrioView.pick_id))
        .filter(*data)
        .group_by(
            Champion.id, Champion.name, PicksBansPrioView.pick_rotation, PicksBansPrioView.side
        )
        .order_by(
            PicksBansPrioView.side,
            PicksBansPrioView.pick_rotation,
            func.count(PicksBansPrioView.pick_id).desc(),
            Champion.name,
        )
    )

    return {
        "blue_picks": [
            {
                "champion_id": row.champion_id,
                "champion_name": row.champion_name,
                "qty_games": row.qty_picks,
                "qty_win": row.qty_win,
                "percent_win": round((row.qty_win / row.qty_picks) * 100, 2),
                "rotation": row.rotation,
            }
            for row in query
            if row.side == "blue"
        ],
        "red_picks": [
            {
                "champion_id": row.champion_id,
                "champion_name": row.champion_name,
                "qty_games": row.qty_picks,
                "qty_win": row.qty_win,
                "percent_win": round((row.qty_win / row.qty_picks) * 100, 2),
                "rotation": row.rotation,
            }
            for row in query
            if row.side == "red"
        ],
    }


@bp.get("bans")
def get_ban_rotation():
    query = list(
        PicksBansPrioView.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("champion_name"),
            PicksBansPrioView.ban_rotation.label("rotation"),
            func.count(PicksBansPrioView.ban_id).label("qty_picks"),
            PicksBansPrioView.side.label("side"),
            func.sum(case((PicksBansPrioView.winner, 1), else_=0)).label("qty_win"),
        )
        .outerjoin((Champion, Champion.id == PicksBansPrioView.ban_id))
        .filter(*filter_pb_data(request, "side"), Champion.id.isnot(None))
        .group_by(
            Champion.id, Champion.name, PicksBansPrioView.ban_rotation, PicksBansPrioView.side
        )
        .order_by(
            PicksBansPrioView.side,
            PicksBansPrioView.ban_rotation,
            func.count(PicksBansPrioView.ban_id).desc(),
            Champion.name,
        )
    )

    return {
        "blue_bans": [
            {
                "champion_id": row.champion_id,
                "champion_name": row.champion_name,
                "qty_games": row.qty_picks,
                "qty_win": row.qty_win,
                "percent_win": round((row.qty_win / row.qty_picks) * 100, 2),
                "rotation": row.rotation,
            }
            for row in query
            if row.side == "blue"
        ],
        "red_bans": [
            {
                "champion_id": row.champion_id,
                "champion_name": row.champion_name,
                "qty_games": row.qty_picks,
                "qty_win": row.qty_win,
                "percent_win": round((row.qty_win / row.qty_picks) * 100, 2),
                "rotation": row.rotation,
            }
            for row in query
            if row.side == "red"
        ],
    }


@bp.get("presence")
def get_champions_presence():
    champions = list(
        PicksBansPrioView.query.with_entities(
            Champion.id.label("id"),
            Champion.name.label("name"),
            PicksBansPrioView.role.label("role"),
        )
        .filter(
            # *filter_pb_data(request)
        )
        .order_by(Champion.name)
        .distinct()
        .outerjoin((Champion, Champion.id == PicksBansPrioView.pick_id))
    )

    pick_presence = (
        PicksBansPrioView.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("champion_name"),
            PicksBansPrioView.role.label("role"),
            func.count(PicksBansPrioView.pick_id).label("qty_picks"),
            func.sum(func.cast(PicksBansPrioView.winner, Integer)).label("qty_win"),
        )
        .outerjoin((Champion, Champion.id == PicksBansPrioView.pick_id))
        .filter(*filter_pb_data(request), Champion.id.isnot(None))
        .group_by(Champion.id, Champion.name, PicksBansPrioView.role)
        .order_by(func.count(PicksBansPrioView.pick_id).desc(), Champion.name)
    )
    pick_dict = [
        {
            "id": row.champion_id,
            "qty_win": row.qty_win,
            "qty_picks": row.qty_picks,
            "role": row.role,
        }
        for row in pick_presence
    ]

    ban_presence = (
        PicksBansPrioView.query.with_entities(
            Champion.id.label("champion_id"),
            Champion.name.label("champion_name"),
            func.count(PicksBansPrioView.ban_id).label("qty_bans"),
        )
        .outerjoin((Champion, Champion.id == PicksBansPrioView.ban_id))
        .filter(*filter_pb_data(request), Champion.id.isnot(None))
        .group_by(
            Champion.id,
            Champion.name,
        )
        .order_by(func.count(PicksBansPrioView.pick_id).desc(), Champion.name)
    )
    ban_dict = [{"id": row.champion_id, "qty_bans": row.qty_bans} for row in ban_presence]
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
    roles = ["baron", "jungle", "mid", "dragon", "sup"]
    data = {r: [] for r in roles}
    for c in champions:
        pick_presence = [row for row in pick_dict if row["role"] == c.role and row["id"] == c.id]
        win_presence = [row for row in pick_dict if row["role"] == c.role and row["id"] == c.id]
        ban_presence = [row for row in ban_dict if row["id"] == c.id]
        if len(pick_presence) > 0 or len(ban_presence):
            qty_picks = 0 if len(pick_presence) == 0 else pick_presence[0]["qty_picks"]
            qty_win = 0 if len(win_presence) == 0 else win_presence[0]["qty_win"]
            qty_bans = 0 if len(ban_presence) == 0 else ban_presence[0]["qty_bans"]
            qty_presence = qty_picks + qty_bans
            _temp = {
                "champion_id": c.id,
                "champion_name": c.name,
                "qty_picks": qty_picks,
                "qty_win": qty_win,
                "qty_presence": qty_presence,
                "percent_win": "-" if qty_picks == 0 else round((qty_win / qty_picks) * 100, 2),
                "percent_presence": "-"
                if qty_presence == 0
                else round((qty_presence / total_games) * 100, 2),
                "qty_bans": qty_bans,
            }
            if c.role is not None:
                data[c.role].append(
                    {**_temp, "total_presence": _temp["qty_picks"] + _temp["qty_bans"]}
                )

    return data
