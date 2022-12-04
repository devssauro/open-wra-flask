from flask import Blueprint, request

from app.db_handler import DBHandler

bp = Blueprint("patch", __name__, url_prefix="/")


@bp.get("/patch")
def get_patches():
    args = request.args
    patches = DBHandler.get_patches(
        tournament=args.getlist("tournament"),
        team=args.getlist("team"),
    )

    return {"patches": patches}
