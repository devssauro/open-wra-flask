from datetime import datetime

import pytest

from app.db_handler.team import LineupTeam
from app.mod_team.models import Team
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


@pytest.fixture
def sample_lieneupteam_list_sample(sample_team_1: Team, sample_team_2: Team) -> list[LineupTeam]:
    return [
        LineupTeam(sample_team_1, []),
        LineupTeam(sample_team_2, []),
    ]


@pytest.fixture
def sample_map_wrong_draft_payload(
    sample_players_payload: dict, sample_wrong_draft_picks_bans_payload
) -> dict:
    return {**sample_wrong_draft_picks_bans_payload, **sample_players_payload}
