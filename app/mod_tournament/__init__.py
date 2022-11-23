from flask import Blueprint


def bp():
    _bp = Blueprint("matchup", __name__, url_prefix="/v1")

    from .routes import champion

    _bp.register_blueprint(champion.bp)
    from .routes import matchup

    _bp.register_blueprint(matchup.bp)
    from .routes import map

    _bp.register_blueprint(map.bp)
    from .routes import patch

    _bp.register_blueprint(patch.bp)
    from .routes import tournament

    _bp.register_blueprint(tournament.bp)

    return _bp
