from flask import Blueprint


def bp():
    _bp = Blueprint("download", __name__, url_prefix="/v1/download")

    from .routes import prio

    _bp.register_blueprint(prio.bp)

    return _bp
