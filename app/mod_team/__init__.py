from flask import Blueprint


def bp():
    _bp = Blueprint("team", __name__, url_prefix="/v1/")

    from .routes import teams

    _bp.register_blueprint(teams.bp)
    from .routes import players

    _bp.register_blueprint(players.bp)

    return _bp
