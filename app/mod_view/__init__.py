from flask import Blueprint


def bp():
    _bp = Blueprint("view", __name__, url_prefix="/v1/view")

    from .routes import champion

    _bp.register_blueprint(champion.bp)
    from .routes import objectives

    _bp.register_blueprint(objectives.bp)
    from .routes import player

    _bp.register_blueprint(player.bp)
    from .routes import prio

    _bp.register_blueprint(prio.bp)
    from .routes import stats

    _bp.register_blueprint(stats.bp)

    return _bp
