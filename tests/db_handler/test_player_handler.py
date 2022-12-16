import pytest

from app.db_handler import PlayerHandler


@pytest.fixture
def player_handler():
    return PlayerHandler()
