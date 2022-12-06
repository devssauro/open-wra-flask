from datetime import datetime

import pytest

from app.mod_tournament.models import Tournament, TournamentTeam


@pytest.fixture
def sample_picks_bans_payload() -> dict:
    """Payload for picks and bans in a match."""
    return {
        "blue_ban_1": 1,
        "red_ban_1": 2,
        "blue_ban_2": 3,
        "red_ban_2": 4,
        "blue_ban_3": 5,
        "red_ban_3": 6,
        "blue_pick_1": 7,
        "red_pick_1": 8,
        "red_pick_2": 9,
        "blue_pick_2": 10,
        "blue_pick_3": 11,
        "red_pick_3": 12,
        "red_ban_4": 13,
        "blue_ban_4": 14,
        "red_ban_5": 15,
        "blue_ban_5": 16,
        "red_pick_4": 17,
        "blue_pick_4": 18,
        "blue_pick_5": 19,
        "red_pick_5": 20,
    }


@pytest.fixture
def sample_wrong_picks_bans_payload(sample_picks_bans_payload: dict) -> dict:
    """Wrong payload with a champion repeated on two parts of picks and bans"""
    return {**sample_picks_bans_payload, "blue_ban_1": 2}


@pytest.fixture
def sample_draft_payload(sample_picks_bans_payload: dict) -> dict:
    """Draft payload with all champions setted for every player"""
    return {
        **sample_picks_bans_payload,
        "blue_baron_pick": sample_picks_bans_payload["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_blue_draft_payload(sample_picks_bans_payload: dict) -> dict:
    """Draft with a mistake on blue team"""
    return {
        **sample_picks_bans_payload,
        "blue_baron_pick": sample_picks_bans_payload["blue_ban_1"],
        "blue_jungle_pick": sample_picks_bans_payload["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_red_draft_payload(sample_picks_bans_payload: dict) -> dict:
    """Draft with a mistake on red team"""
    return {
        **sample_picks_bans_payload,
        "blue_baron_pick": sample_picks_bans_payload["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload["red_ban_1"],
        "red_jungle_pick": sample_picks_bans_payload["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload["red_pick_5"],
    }


@pytest.fixture
def sample_players_payload() -> dict:
    """Draft payload with all player for the two teams"""
    return {
        "blue_baron_player": 1,
        "blue_jungle_player": 2,
        "blue_mid_player": 3,
        "blue_dragon_player": 4,
        "blue_sup_player": 5,
        "red_baron_player": 6,
        "red_jungle_player": 7,
        "red_mid_player": 8,
        "red_dragon_player": 9,
        "red_sup_player": 10,
    }


@pytest.fixture
def sample_wrong_players_payload(sample_players_payload: dict) -> dict:
    """Draft payload with a player setted in two positions"""
    return {
        **sample_players_payload,
        "blue_baron_player": sample_players_payload["blue_jungle_player"],
    }


@pytest.fixture
def sample_tournament_payload_1() -> dict:
    return {
        "name": "Tournament 1",
        "tag": "TEST",
        "start_date": datetime(2022, 12, 4),
        "end_date": datetime(2023, 1, 4),
        "lineups": [
            {"team_id": 1, "entry_phase": "playoffs", "players": []},
        ],
        "region": "br",
        "split": "1",
        "phases": "group,playoffs,final",
    }


@pytest.fixture
def sample_tournament_payload_2(sample_tournament_payload_1) -> dict:
    sample_tournament_payload_1["name"] = "Tournament 2"
    sample_tournament_payload_1["split"] = "2"
    sample_tournament_payload_1["phases"] = [
        {"name": "group", "bo_size": 3, "with_global_ban": True, "last_no_global_ban": False},
        {
            "name": "quarterfinals",
            "bo_size": 5,
            "with_global_ban": True,
            "last_no_global_ban": False,
        },
        {"name": "semifinals", "bo_size": 5, "with_global_ban": True, "last_no_global_ban": True},
        {"name": "final", "bo_size": 7, "with_global_ban": True, "last_no_global_ban": True},
    ]
    return sample_tournament_payload_1


@pytest.fixture
def sample_tournament_payload_3(sample_tournament_payload_1) -> dict:
    sample_tournament_payload_1["name"] = "Tournament 3"
    sample_tournament_payload_1["phases"] = ["group", "knockout", "final"]
    return sample_tournament_payload_1


@pytest.fixture
def sample_tournament_team_1() -> TournamentTeam:
    team = TournamentTeam(team_id=1, tournament_id=1, entry_phase="group")
    team.id = 1
    return team


@pytest.fixture
def sample_tournament_1(
    sample_tournament_payload_1, sample_tournament_team_1: TournamentTeam
) -> Tournament:
    del sample_tournament_payload_1["lineups"]
    tournament = Tournament(**sample_tournament_payload_1)
    tournament.id = 1
    tournament.teams = [sample_tournament_team_1]
    return tournament


@pytest.fixture
def sample_tournament_2(
    sample_tournament_payload_2, sample_tournament_team_1: TournamentTeam
) -> Tournament:
    del sample_tournament_payload_2["lineups"]
    tournament = Tournament.from_payload(None, **sample_tournament_payload_2)
    tournament.id = 2
    tournament.teams = [sample_tournament_team_1]
    return tournament
