from datetime import datetime
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from decouple import config
from flask import Flask
from flask_security import hash_password

from app import create_app
from app.mod_auth.models import Role, User


@pytest.fixture(autouse=True)
def create_test_database():
    """Create fresh test database for each test in this package"""
    c = Config("migrations/alembic.ini")
    c.set_main_option("script_location", "migrations")
    c.set_main_option("sqlalchemy.url", config("SQLALCHEMY_DATABASE_TEST_URI"))
    command.upgrade(c, "head")
    yield
    command.downgrade(c, "base")


@pytest.fixture
def app() -> Flask:
    """Sample flask app for API testing."""
    app = create_app(True)
    app.config.update(
        {
            "TESTING": True,
            "SECURITY_PASSWORD_HASH": "plaintext",
        }
    )
    app.app_context().push()
    yield app


@pytest.fixture
def sample_app(app, create_test_database):
    """Sample app in test client for automated testing."""
    return app.test_client()


@pytest.fixture
def sample_user(sample_app) -> User:
    """Sample user to attribute profiles and test permissions."""
    user = User()
    user.email = "cunha.ladm@outlook.com"
    user.password = hash_password("123546")
    user.username = "devssauro"
    user.fs_uniquifier = uuid4().hex
    user.confirmed_at = datetime.now()
    return user


@pytest.fixture
def sample_admin_profile() -> Role:
    """Sample admin profile to assert permissions."""
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
    """Sample user with admin profile."""
    sample_user.roles = [sample_admin_profile]
    sample_user.id = 1
    return sample_user
