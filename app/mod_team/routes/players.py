from flask import Blueprint, request
from flask_security import roles_accepted

from db_config import db

from ..models import Player

bp = Blueprint("player", __name__, url_prefix="player")
roles = {"1": "baron", "2": "jungle", "3": "mid", "4": "dragon", "5": "sup"}


@bp.get("")
@roles_accepted("operational", "admin")
def get_players():
    args = []
    players = (
        Player.query.with_entities(
            Player.id,
            Player.nickname,
            Player.flag,
            Player.team_id,
            Player.role,
        )
        .filter(*args)
        .order_by(Player.nickname)
    )

    return {
        "players": [
            dict(
                id=player.id,
                nickname=player.nickname,
                flag=player.flag,
                role=None if not player.role else player.role.name,
            )
            for player in players
        ]
    }


@bp.post("")
@roles_accepted("operational", "admin")
def post_player():
    player: Player = Player(**request.json)
    db.session.add(player)
    db.session.commit()

    return {"id": player.id}, 201


@bp.put("")
@roles_accepted("operational", "admin")
def put_player():
    if "id" not in request.json:
        return {"msg": "id is missing"}

    player: Player = Player.query.get(request.json["id"])
    player.name = request.json["nickname"]
    player.role = request.json["role"]
    player.flag = request.json["flag"]
    db.session.add(player)
    db.session.commit()

    return {"msg": "Player has changed"}
