import pytest
from alembic import command
from alembic.config import Config


@pytest.fixture(autouse=True)
def create_test_database():
    """Create fresh test database for each test in this package"""
    c = Config("migrations/alembic.ini")
    c.set_main_option("script_location", "migrations")
    command.upgrade(c, "head")
    yield
    command.downgrade(c, "base")
