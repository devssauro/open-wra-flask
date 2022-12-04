from datetime import datetime

import pytest

from app.db_handler.team import LineupTeam
from app.mod_team.models import Team
from app.mod_tournament.models import Champion, Matchup


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


@pytest.fixture
def sample_matchup_payload() -> dict:
    return {
        "datetime": datetime(2022, 12, 4, 18, 0),
        "phase": "group",
        "mvp_id": None,
        "team1_id": 1,
        "team2_id": 2,
    }


@pytest.fixture
def sample_team_1() -> Team:
    """Team object for Matchup"""
    team = Team(name="Team 1", tag="T1", flag="KR")
    team.id = 1
    team.active = True
    team.date_created = datetime(2022, 12, 3)
    team.date_updated = datetime(2022, 12, 3)
    return team


@pytest.fixture
def sample_team_2(sample_team_1: Team) -> Team:
    """Team object for Matchup"""
    sample_team_1.id = 2
    sample_team_1.tag = "T2"
    sample_team_1.name = "Team 2"
    sample_team_1.date_created = datetime(2022, 12, 3)
    sample_team_1.date_updated = datetime(2022, 12, 3)
    return sample_team_1


@pytest.fixture
def sample_matchup_1(
    sample_matchup_payload: dict,
    sample_team_1: Team,
    sample_team_2: Team,
) -> Matchup:
    matchup = Matchup(**sample_matchup_payload)
    matchup.id = 1
    matchup.team1 = sample_team_1
    matchup.team2 = sample_team_2
    return matchup


@pytest.fixture
def sample_lieneupteam_list_sample(sample_team_1: Team, sample_team_2: Team) -> list[LineupTeam]:
    return [
        LineupTeam(sample_team_1, []),
        LineupTeam(sample_team_2, []),
    ]
