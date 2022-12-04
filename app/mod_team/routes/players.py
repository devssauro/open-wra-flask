from flask import Blueprint, request
from flask_security import roles_accepted

from app.db_handler import DBHandler
from app.mod_team.models import Player

bp = Blueprint("player", __name__, url_prefix="player")
roles = {"1": "baron", "2": "jungle", "3": "mid", "4": "dragon", "5": "sup"}


@bp.get("")
@roles_accepted("operational", "admin")
def get_players():
    args = request.args
    result = DBHandler.get_players(
        args.get("nickname"),
        args.get("region"),
        args.get("page", 1),
        args.get("per_page", 10),
    )
    return {
        "players": [player.to_dict() for player in result.players],
        "pages": result.pages,
        "page": result.page,
    }


@bp.post("")
@roles_accepted("operational", "admin")
def post_player():
    player = Player(**request.json)
    player = DBHandler.create_update_player(player)

    return {"id": player.id}, 201


@bp.put("/<int:player_id>")
@roles_accepted("operational", "admin")
def put_player(player_id: int):

    player = DBHandler.get_player_by_id(player_id)
    if not player:
        return {"msg": "Player not found"}, 404

    player.nickname = request.json.get("nickname", player.nickname)
    player.role = request.json.get("role", player.role)
    player.flag = request.json.get("flag", player.flag)

    DBHandler.create_update_player(player)

    return {"msg": "Player has changed"}
