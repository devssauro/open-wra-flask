from flask import Blueprint, request
from flask_security import roles_accepted
from sqlalchemy import and_, or_

from app.mod_view.models import ObjectiveView, PicksBansPrioView
from app.mod_view.utils import filter_by_id, team_expression_resolver

bp = Blueprint("objectives", __name__, url_prefix="/objectives")

OBJECTIVE_FIELDS = ("drake", "herald", "first_tower", "first_blood")
DRAFT_FIELDS = ("pick", "ban")
ROTATION_FIELDS = {
    "B1": and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 1),
    "B2/B3": and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 2),
    "B4/B5": and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 3),
    "R1/R2": and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 1),
    "R3": and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 2),
    "R4": and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 3),
    "R5": and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 4),
}
ID_FIELDS = (
    "player",
    "champion",
    "player_killer",
    "champion_killer",
    "player_victim",
    "champion_victim",
)
PARAMS = {
    "drake": {
        "order": {n: ObjectiveView.objective_order == n for n in (1, 2, 3)},
        "name": {n: ObjectiveView.objective_name == n for n in ("ocean", "mountain", "infernal")},
        "with_teamfight": {n: ObjectiveView.with_teamfight == n for n in (True, False)},
        "is_stealed": {n: ObjectiveView.is_stealed == n for n in (True, False)},
    },
    "herald": {
        "order": {n: ObjectiveView.objective_order == n for n in (1, 2)},
        "with_teamfight": {n: ObjectiveView.with_teamfight == n for n in (True, False)},
        "is_stealed": {n: ObjectiveView.is_stealed == n for n in (True, False)},
        "place": {n: ObjectiveView.place == n for n in (1, 2, 3)},
    },
    "first_tower": {
        "with_herald": {n: ObjectiveView.with_herald == n for n in (True, False)},
        "place": {n: ObjectiveView.place == n for n in ("baron", "mid", "dragon")},
        "name": {n: ObjectiveView.objective_name == n for n in ("baron", "mid", "dragon")},
    },
    "first_blood": {
        "place": {
            n: ObjectiveView.place == n
            for n in (  # DONE
                "baron lane",
                "mid lane",
                "dragon lane",
                "baron river",
                "dragon river",
                "blue jungle",
                "red jungle",
            )
        },
        "player_killer": lambda killer: filter_by_id(ObjectiveView.killer, killer),
        "champion_killer": lambda killer: filter_by_id(ObjectiveView.champion_killer, killer),
        "role_killer": {
            n: ObjectiveView.role_killer == n for n in ("baron", "jungle", "mid", "dragon", "sup")
        },
        "player_victim": lambda victim: filter_by_id(ObjectiveView.victim, victim),
        "champion_victim": lambda victim: filter_by_id(ObjectiveView.champion_victim, victim),
        "role_victim": {
            n: ObjectiveView.role_victim == n for n in ("baron", "jungle", "mid", "dragon", "sup")
        },
    },
    "pick": {
        "side": {n: PicksBansPrioView.side == n for n in ("blue", "red")},
        "is_blind": {n: PicksBansPrioView.is_blind == n for n in (True, False)},
        "rotation": {
            n: ROTATION_FIELDS[n] for n in ("B1", "B2/B3", "B4/B5", "R1/R2", "R3", "R4", "R5")
        },
        "role": {
            n: PicksBansPrioView.role == n for n in ("baron", "jungle", "mid", "dragon", "sup")
        },
        "position": (1, 2, 3, 4, 5),
        "player": lambda player: filter_by_id(PicksBansPrioView.player, player),
        "champion": lambda champion: filter_by_id(PicksBansPrioView.pick_id, champion),
        "chained": (True, False),
    },
    "ban": {
        "side": {n: PicksBansPrioView.side == n for n in ("blue", "red")},
        "rotation": {n: PicksBansPrioView.ban_rotation == n for n in (1, 2)},
        "position": (1, 2, 3, 4, 5),
        "champion": lambda champion: filter_by_id(PicksBansPrioView.ban_id, champion),
        "chained": (True, False),
    },
}

view = {
    **{param: ObjectiveView for param in OBJECTIVE_FIELDS},
    **{param: PicksBansPrioView for param in DRAFT_FIELDS},
}


@bp.post("")
@roles_accepted("analyst", "admin")
def objectives():
    """Criar um pseudo formato de query"""

    conditions = request.json.get("conditions")
    default = request.json.get("default", None)
    filters = []
    if "t" in request.args:
        if conditions[0]["type"] in OBJECTIVE_FIELDS:
            filters.append(ObjectiveView.tournament_id.in_(request.args.getlist("t")))
        if conditions[0]["type"] in DRAFT_FIELDS:
            filters.append(PicksBansPrioView.tournament_id.in_(request.args.getlist("t")))

    team_field = {
        "taker": ObjectiveView.team_id,
        "giver": ObjectiveView.team_giver_id,
        "-": ObjectiveView.team_id,
    }

    maps = []
    start = True

    unchained_conditions = [
        condition for condition in conditions if not condition.get("chained", True)
    ]
    unchained_maps = []
    chained_conditions = [condition for condition in conditions if condition.get("chained", True)]
    for condition in unchained_conditions:
        if condition.get("type") in PARAMS.keys():
            for param in condition.keys():
                if param not in ("type", "chained"):
                    if param in ID_FIELDS:
                        filters.append(PARAMS[condition["type"]][param](condition[param]))
                    else:
                        filters.append(PARAMS[condition["type"]][param][condition[param]])
            query = (
                PicksBansPrioView.query.distinct(PicksBansPrioView.map_id)
                .with_entities(PicksBansPrioView.map_id)
                .filter(
                    *filters, PicksBansPrioView.map_id.in_(unchained_maps) if not start else True
                )
                .order_by(PicksBansPrioView.map_id)
            )

            unchained_maps = [q.map_id for q in query]
            if len(maps) == 0 and not start:
                break
            start = False
            filters = []

    if len(unchained_maps) > 0 and len(chained_conditions) > 0:
        filters.append(
            ObjectiveView.map_id.in_(unchained_maps)
            if chained_conditions[0]["type"] in OBJECTIVE_FIELDS
            else PicksBansPrioView.map_id.in_(unchained_maps)
        )
    else:
        maps = unchained_maps

    for condition in chained_conditions:
        if condition.get("type") in PARAMS.keys():
            for param in condition.keys():
                if param not in ("type", "chained"):
                    if param in ID_FIELDS:
                        filters.append(PARAMS[condition["type"]][param](condition[param]))
                    else:
                        if type(condition[param]) in (list, tuple):
                            filters.append(
                                or_(
                                    *[
                                        PARAMS[condition["type"]][param][_p]
                                        for _p in condition[param]
                                    ]
                                )
                            )
                        else:
                            filters.append(PARAMS[condition["type"]][param][condition[param]])
            query = (
                ObjectiveView.query.distinct(ObjectiveView.map_id)
                .with_entities(
                    ObjectiveView.map_id,
                    team_field.get("team", team_field[default]).label("team_id"),
                )
                .filter(
                    *filters,
                    or_(
                        *[
                            and_(
                                ObjectiveView.map_id == map["map_id"],
                                team_expression_resolver(
                                    condition.get("team", default), map["team_id"]
                                ),
                            )
                            for map in maps
                        ]
                    )
                )
                .order_by(ObjectiveView.map_id)
                if condition["type"] in OBJECTIVE_FIELDS
                else PicksBansPrioView.query.distinct(PicksBansPrioView.map_id)
                .with_entities(PicksBansPrioView.map_id, PicksBansPrioView.team_id)
                .filter(
                    *filters,
                    or_(
                        *[
                            and_(
                                PicksBansPrioView.map_id == map["map_id"],
                                PicksBansPrioView.team_id == map["team_id"],
                            )
                            for map in maps
                        ]
                    )
                )
                .order_by(PicksBansPrioView.map_id)
            )

            maps = [{"map_id": q.map_id, "team_id": q.team_id} for q in query]
            maps = (
                maps if condition.get("team") != "-" else [m for m in maps if m["team_id"] is None]
            )
            if len(maps) == 0 and not start:
                break
            start = False
            filters = []

    if len(chained_conditions) > 0:
        maps = [_map["map_id"] for _map in maps]

    return {"maps": maps}
