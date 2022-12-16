from decouple import config as d_config
from flask import Flask
from flask_cors import CORS

from db_config import db, migrate
from jwt_config import jwt
from mail_config import mail
from security_config import security, user_datastore

from . import config


def create_app(is_testing: bool = False):
    app = Flask(
        __name__,
        instance_relative_config=True,
    )
    if is_testing:
        config.SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_TEST_URI
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    # csrf.init_app(app)
    security.init_app(app, user_datastore)
    jwt.init_app(app)

    app.config.update(
        {
            "MAIL_PORT": d_config("MAIL_PORT"),
            "MAIL_SERVER": d_config("MAIL_SERVER"),
            "MAIL_USE_SSL": d_config("MAIL_USE_SSL", cast=bool),
            "MAIL_USE_TLS": d_config("MAIL_USE_TLS", cast=bool),
            "MAIL_USERNAME": d_config("MAIL_USERNAME"),
            "MAIL_PASSWORD": d_config("MAIL_PASSWORD"),
        }
    )

    mail.init_app(app)

    CORS(
        app,
        supports_credentials=True,  # needed for cross domain cookie support
        resources="/*",
        allow_headers="*",
        origins=d_config("CORS_ORIGINS"),
        expose_headers="Authorization,Content-Type,Authentication-Token,XSRF-TOKEN",
    )

    @app.get("/")
    def hello():
        return "hello"

    # if test_config is None:
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     app.config.from_mapping(test_config)

    from . import mod_auth

    app.register_blueprint(mod_auth.bp)
    from . import mod_download

    app.register_blueprint(mod_download.bp())
    from . import mod_team

    app.register_blueprint(mod_team.bp())
    from . import mod_tournament

    app.register_blueprint(mod_tournament.bp())
    from . import mod_view

    app.register_blueprint(mod_view.bp())

    return app
