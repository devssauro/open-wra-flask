from flask import Blueprint, request
from flask_security import roles_accepted

from db_config import db

from ..models import Matchup, MatchupMap

bp = Blueprint("map", __name__, url_prefix="matchup/<int:matchup_id>/map")


@bp.post("")
@roles_accepted("operational", "admin")
def post_map(matchup_id: int):
    matchup: Matchup = Matchup.query.get(matchup_id)
    data = {**request.json}
    if "team_first_death" in request.json:
        del data["team_first_death"]
    _map: MatchupMap = MatchupMap.from_payload(**{**data, "tournament_id": matchup.tournament_id})
    _map.matchup_id = matchup_id
    _map.map_number = len(matchup.maps) + 1
    db.session.add(_map)
    db.session.commit()

    return {"map_id": _map.id}, 201


@bp.get("/<int:map_id>/edit")
def get_map_id(matchup_id: int, map_id: int):
    matchup: MatchupMap = MatchupMap.query.filter(
        MatchupMap.matchup_id == matchup_id, MatchupMap.id == map_id
    ).first()

    if not matchup:
        return {"msg": "Map not found"}, 404

    _map = matchup.to_dict(
        rules=("-matchup", "-uuid", "-active", "-id", "-date_created", "-date_modified", "-extra")
    )
    _map["first_tower_route"] = matchup.first_tower_route.name
    return _map, 200


@bp.put("/<int:map_id>/edit")
def put_map_id(matchup_id: int, map_id: int):
    matchup: MatchupMap = MatchupMap.query.filter(
        MatchupMap.matchup_id == matchup_id, MatchupMap.id == map_id
    ).first()

    if not matchup:
        return {"msg": "Map not found"}, 404

    matchup.update(request.json)
    db.session.commit()
    _map = matchup.to_dict(
        rules=("-matchup", "-uuid", "-active", "-id", "-date_created", "-date_modified", "-extra")
    )
    _map["first_tower_route"] = matchup.first_tower_route.name
    return _map, 200
