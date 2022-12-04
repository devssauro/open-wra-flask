from datetime import datetime

import pytest

from app.mod_tournament.models import Champion


@pytest.fixture
def sample_champion_1() -> Champion:
    """Sample champion object."""
    champion = Champion()
    champion.id = 1
    champion.name = "Ahri"
    champion.date_create = datetime(2022, 12, 4)
    champion.date_update = datetime(2022, 12, 4)
    return champion


@pytest.fixture
def sample_patch_1() -> str:
    return "3.5a"
