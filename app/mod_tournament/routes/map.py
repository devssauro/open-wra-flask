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
    map: MatchupMap = MatchupMap(**{**data, "tournament_id": matchup.tournament_id})
    map.matchup_id = matchup_id
    map.map_number = len(matchup.maps) + 1
    db.session.add(map)
    db.session.commit()

    return {"map_id": map.id}, 201


@bp.get("/<int:map_id>/edit")
def get_map_id(matchup_id: int, map_id: int):
    matchup: MatchupMap = MatchupMap.query.filter(
        MatchupMap.matchup_id == matchup_id, MatchupMap.id == map_id
    ).first()

    if not matchup:
        return {"msg": "Map not found"}, 404

    map = matchup.to_dict(
        rules=("-matchup", "-uuid", "-active", "-id", "-date_created", "-date_modified", "-extra")
    )
    map["first_tower_route"] = matchup.first_tower_route.name
    return map, 200


@bp.put("/<int:map_id>/edit")
def put_map_id(matchup_id: int, map_id: int):
    matchup: MatchupMap = MatchupMap.query.filter(
        MatchupMap.matchup_id == matchup_id, MatchupMap.id == map_id
    ).first()

    if not matchup:
        return {"msg": "Map not found"}, 404

    matchup.update(request.json)
    db.session.commit()
    map = matchup.to_dict(
        rules=("-matchup", "-uuid", "-active", "-id", "-date_created", "-date_modified", "-extra")
    )
    map["first_tower_route"] = matchup.first_tower_route.name
    return map, 200
