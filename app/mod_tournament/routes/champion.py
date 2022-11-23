from flask import Blueprint, request

from ..models import Champion

bp = Blueprint("champion", __name__, url_prefix="/champion")


@bp.get("")
def get_champions():
    args = []
    if request.args.get("s"):
        args.append(Champion.name.contains(request.args["s"]))
    champions = Champion.query.filter(*args).order_by(Champion.name)

    return {"champions": [champion.to_dict() for champion in champions]}
