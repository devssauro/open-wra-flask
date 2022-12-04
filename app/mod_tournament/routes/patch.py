from flask import Blueprint, request

from app.db_handler import DBHandler

bp = Blueprint("patch", __name__, url_prefix="/")


@bp.get("/patch")
def get_patches():
    patches = DBHandler.get_patches(request)

    return {"patches": patches}
