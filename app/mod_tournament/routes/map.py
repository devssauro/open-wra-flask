from flask import Blueprint, request

from app.db_handler import DBHandler
from app.exceptions import DraftIntegrityError, GlobalBanError, LineupIntegrityError
from app.mod_download.utils import ROLES
from app.mod_tournament.models import MatchupMap
from app.mod_tournament.models.abstracts import SIDES

bp = Blueprint("map", __name__, url_prefix="matchup/<int:matchup_id>/map")


@bp.post("")
# @roles_accepted("operational", "admin")
def post_map(matchup_id: int):
    matchup = DBHandler.get_matchup_by_id(matchup_id)
    if matchup is None:
        return {"msg": "Matchup not found"}, 404

    data = {**request.json}
    if "team_first_death" in request.json:
        del data["team_first_death"]

    try:
        for role in ROLES:
            for side in SIDES:
                data[f"{side}_{role}_dmg_taken"] = int(data[f"{side}_{role}_dmg_taken"]) * int(
                    int(data[f"{side}_{role}_deaths"]) + 1
                )
        _map: MatchupMap = MatchupMap.from_payload(
            **{**data, "tournament_id": matchup.tournament_id}
        )
    except DraftIntegrityError as e:
        return {"msg": e.message}, 406
    except LineupIntegrityError as e:
        return {"msg": e.message}, 406

    _map.matchup_id = matchup_id
    _map.map_number = len(matchup.maps) + 1

    try:
        matchup.add_map(_map)
    except GlobalBanError as e:
        return {
            "msg": e.message,
            "team_id": e.team_id,
            "champion_id": e.champion_id,
        }, 406

    _map = DBHandler.create_update_map(_map)

    return {"map_id": _map.id}, 201


@bp.get("/<int:map_id>/edit")
# @roles_accepted("operational", "admin")
def get_map_id(matchup_id: int, map_id: int):
    matchup = DBHandler.get_map_by_id(map_id)

    if matchup is None:
        return {"msg": "Map not found"}, 404

    _map = matchup.to_dict(
        rules=("-matchup", "-uuid", "-active", "-date_created", "-date_modified", "-extra")
    )
    if matchup.first_tower_route is not None:
        _map["first_tower_route"] = matchup.first_tower_route.name
    return _map, 200


@bp.put("/<int:map_id>/edit")
# @roles_accepted("operational", "admin")
def put_map_id(matchup_id: int, map_id: int):
    matchup = DBHandler.get_map_by_id(map_id)

    if not matchup:
        return {"msg": "Map not found"}, 404

    data = request.json
    for role in ROLES:
        for side in SIDES:
            data[f"{side}_{role}_dmg_taken"] = int(data[f"{side}_{role}_dmg_taken"]) * int(
                data[f"{side}_{role}_deaths"] + 1
            )
    MatchupMap.from_payload(matchup, **data)
    matchup = DBHandler.create_update_map(matchup)

    _map = matchup.to_dict(
        rules=("-matchup", "-uuid", "-active", "-date_created", "-date_modified", "-extra")
    )
    if matchup.first_tower_route is not None:
        _map["first_tower_route"] = matchup.first_tower_route.name

    return _map, 200
