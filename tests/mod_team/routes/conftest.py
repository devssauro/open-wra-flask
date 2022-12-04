from datetime import datetime

import pytest

from app.mod_team.models import Player, Team


@pytest.fixture
def sample_team_payload() -> dict:
    """Payload for a team"""
    return {"name": "Team 1", "tag": "T1", "flag": "KR"}


@pytest.fixture
def sample_team_1(sample_team_payload: dict) -> Team:
    """Team object to be managed from DBHandler"""
    team = Team(**sample_team_payload)
    team.id = 1
    team.active = True
    team.date_created = datetime(2022, 12, 3)
    team.date_updated = datetime(2022, 12, 3)
    return team


@pytest.fixture
def sample_player_payload() -> dict:
    """Payload for a player"""
    return {"nickname": "Player 1", "flag": "KR"}


@pytest.fixture
def sample_player_1(sample_player_payload: dict) -> Player:
    """Player object to be managed from DBHandler"""
    player = Player(**sample_player_payload)
    player.id = 1
    player.active = True
    player.date_created = datetime(2022, 12, 3)
    player.date_updated = datetime(2022, 12, 3)
    return player
