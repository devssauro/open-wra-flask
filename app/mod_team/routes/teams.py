from flask import Blueprint, request

from app.db_handler import DBHandler
from app.mod_team.models import Team

bp = Blueprint("team", __name__, url_prefix="/team")


@bp.get("")
def get_team():
    args = request.args
    result = DBHandler.get_teams(
        args.get("tag"), args.get("flag"), args.get("page", 1), args.get("per_page", 10)
    )

    return {
        "teams": [team.to_dict() for team in result.teams],
        "pages": result.pages,
        "page": result.page,
    }


@bp.post("")
# @roles_accepted("operational", "admin")
def post_team():
    team = Team(**request.json)
    team = DBHandler.create_update_team(team)

    return {"id": team.id}, 201


@bp.put("/<int:team_id>")
# @roles_accepted("operational", "admin")
def put_team(team_id: int):
    team = DBHandler.get_team_by_id(team_id)
    if team is None:
        return {"msg": "Team not found"}, 404

    team.name = request.json["name"]
    team.tag = request.json["tag"]
    team.flag = request.json["flag"]

    DBHandler.create_update_team(team)

    return {"msg": "Team has changed"}
