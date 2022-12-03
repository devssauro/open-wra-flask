from datetime import datetime

import pytest

from app.mod_team.models import Team


@pytest.fixture
def sample_team_payload() -> dict:
    """Payload for a team"""
    return {"name": "Team 1", "tag": "T1", "flag": "KR"}


@pytest.fixture
def sample_team_1(sample_team_payload: Team) -> Team:
    team = Team(**sample_team_payload)
    team.id = 1
    team.active = True
    team.date_created = datetime(2022, 12, 3)
    team.date_updated = datetime(2022, 12, 3)
    return team
