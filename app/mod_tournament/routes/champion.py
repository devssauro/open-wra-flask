from flask import Blueprint

from app.db_handler import DBHandler

bp = Blueprint("champion", __name__, url_prefix="/champion")


@bp.get("")
def get_champions():
    champions = DBHandler.get_champions()
    return {"champions": [champion.to_dict() for champion in champions]}
