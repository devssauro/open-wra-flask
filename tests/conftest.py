from datetime import datetime
from uuid import uuid4

import pytest
from flask import Flask
from flask_security import hash_password

from app import create_app
from app.mod_auth.models import Role, User


@pytest.fixture
def app() -> Flask:
    """Sample flask app for API testing."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SECURITY_PASSWORD_HASH": "plaintext",
        }
    )
    app.app_context().push()
    yield app


@pytest.fixture
def sample_app(app):
    return app.test_client()


@pytest.fixture
def sample_user(sample_app) -> User:
    user = User()
    user.email = "cunha.ladm@outlook.com"
    user.password = hash_password("123546")
    user.username = "devssauro"
    user.fs_uniquifier = uuid4().hex
    user.confirmed_at = datetime.now()
    return user


@pytest.fixture
def sample_admin_profile() -> Role:
    admin = Role()
    admin.name = "admin"
    admin.description = "Administrador"
    admin.permissions = ",".join(
        {
            "admin-read",
            "admin-write",
            "admin-update",
            "admin-remove",
            "op-read",
            "analyst-read",
        }
    )
    return admin


@pytest.fixture
def sample_admin_user(sample_user, sample_admin_profile) -> User:
    sample_user.roles = [sample_admin_profile]
    sample_user.id = 1
    return sample_user
