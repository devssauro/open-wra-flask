from datetime import datetime

import pytest

from app.mod_team.models import Team
from app.mod_tournament.models import Matchup, MatchupMap, Tournament, TournamentTeam


@pytest.fixture
def sample_picks_bans_payload_1() -> dict:
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
def sample_picks_bans_payload_2(sample_picks_bans_payload_1) -> dict:
    """Payload for picks and bans in a match."""
    return {
        key: sample_picks_bans_payload_1[key] + 20 for key in sample_picks_bans_payload_1.keys()
    }


@pytest.fixture
def sample_wrong_picks_bans_payload(sample_picks_bans_payload_1) -> dict:
    """Wrong payload with a champion repeated on two parts of picks and bans"""
    return {**sample_picks_bans_payload_1, "blue_ban_1": 2}


@pytest.fixture
def sample_draft_payload_1(sample_picks_bans_payload_1) -> dict:
    """Draft payload with all champions setted for every player"""
    return {
        **sample_picks_bans_payload_1,
        "blue_baron_pick": sample_picks_bans_payload_1["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload_1["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload_1["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_1["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_1["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload_1["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload_1["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_1["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_1["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_1["red_pick_5"],
    }


@pytest.fixture
def sample_draft_payload_2(sample_picks_bans_payload_2) -> dict:
    """Draft payload with all champions setted for every player"""
    return {
        **sample_picks_bans_payload_2,
        "blue_baron_pick": sample_picks_bans_payload_2["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload_2["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload_2["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_2["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_2["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload_2["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload_2["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_2["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_2["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_2["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_draft_picks_bans_payload(sample_wrong_picks_bans_payload: dict) -> dict:
    """Draft payload with all champions setted for every player
    but with a champion double picked.
    """
    return {
        **sample_wrong_picks_bans_payload,
        "blue_baron_pick": sample_wrong_picks_bans_payload["blue_pick_1"],
        "blue_jungle_pick": sample_wrong_picks_bans_payload["blue_pick_2"],
        "blue_mid_pick": sample_wrong_picks_bans_payload["blue_pick_3"],
        "blue_dragon_pick": sample_wrong_picks_bans_payload["blue_pick_4"],
        "blue_sup_pick": sample_wrong_picks_bans_payload["blue_pick_5"],
        "red_baron_pick": sample_wrong_picks_bans_payload["red_pick_1"],
        "red_jungle_pick": sample_wrong_picks_bans_payload["red_pick_2"],
        "red_mid_pick": sample_wrong_picks_bans_payload["red_pick_3"],
        "red_dragon_pick": sample_wrong_picks_bans_payload["red_pick_4"],
        "red_sup_pick": sample_wrong_picks_bans_payload["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_draft_payload(sample_picks_bans_payload_1) -> dict:
    """Draft payload with all champions setted for every player,
    but a champion is double picked"""
    return {
        **sample_picks_bans_payload_1,
        "blue_baron_pick": sample_picks_bans_payload_1["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload_1["blue_pick_1"],
        "blue_mid_pick": sample_picks_bans_payload_1["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_1["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_1["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload_1["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload_1["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_1["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_1["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_1["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_blue_side_payload(sample_picks_bans_payload_1) -> dict:
    """Draft payload with all champions setted for every player,
    but a non-picked champion is set on blue side"""
    return {
        **sample_picks_bans_payload_1,
        "blue_baron_pick": 99,
        "blue_jungle_pick": sample_picks_bans_payload_1["blue_pick_1"],
        "blue_mid_pick": sample_picks_bans_payload_1["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_1["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_1["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload_1["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload_1["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_1["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_1["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_1["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_red_side_payload(sample_picks_bans_payload_1) -> dict:
    """Draft payload with all champions setted for every player,
    but a non-picked champion is set on red side"""
    return {
        **sample_picks_bans_payload_1,
        "blue_baron_pick": sample_picks_bans_payload_1["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload_1["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload_1["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_1["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_1["blue_pick_5"],
        "red_baron_pick": 99,
        "red_jungle_pick": sample_picks_bans_payload_1["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_1["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_1["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_1["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_blue_draft_payload(sample_picks_bans_payload_1) -> dict:
    """Draft with a mistake on blue team"""
    return {
        **sample_picks_bans_payload_1,
        "blue_baron_pick": sample_picks_bans_payload_1["blue_ban_1"],
        "blue_jungle_pick": sample_picks_bans_payload_1["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload_1["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_1["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_1["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload_1["red_pick_1"],
        "red_jungle_pick": sample_picks_bans_payload_1["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_1["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_1["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_1["red_pick_5"],
    }


@pytest.fixture
def sample_wrong_red_draft_payload(sample_picks_bans_payload_1) -> dict:
    """Draft with a mistake on red team"""
    return {
        **sample_picks_bans_payload_1,
        "blue_baron_pick": sample_picks_bans_payload_1["blue_pick_1"],
        "blue_jungle_pick": sample_picks_bans_payload_1["blue_pick_2"],
        "blue_mid_pick": sample_picks_bans_payload_1["blue_pick_3"],
        "blue_dragon_pick": sample_picks_bans_payload_1["blue_pick_4"],
        "blue_sup_pick": sample_picks_bans_payload_1["blue_pick_5"],
        "red_baron_pick": sample_picks_bans_payload_1["red_ban_1"],
        "red_jungle_pick": sample_picks_bans_payload_1["red_pick_2"],
        "red_mid_pick": sample_picks_bans_payload_1["red_pick_3"],
        "red_dragon_pick": sample_picks_bans_payload_1["red_pick_4"],
        "red_sup_pick": sample_picks_bans_payload_1["red_pick_5"],
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
    """Draft payload with a player set in two positions"""
    return {
        **sample_players_payload,
        "blue_baron_player": sample_players_payload["blue_jungle_player"],
    }


@pytest.fixture
def sample_draft_wrong_players_payload(
    sample_draft_payload_1, sample_wrong_players_payload: dict
) -> dict:
    """Payload with player set in two positions"""
    return {**sample_draft_payload_1, **sample_wrong_players_payload}


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
def sample_map_payload_1(sample_players_payload: dict, sample_draft_payload_1) -> dict:
    return {**sample_draft_payload_1, **sample_players_payload}


@pytest.fixture
def sample_map_payload_2(sample_players_payload: dict, sample_draft_payload_2) -> dict:
    return {**sample_draft_payload_2, **sample_players_payload}


@pytest.fixture
def sample_matchup_payload() -> dict:
    return {
        "tournament_id": 1,
        "datetime": datetime(2022, 12, 4, 18, 0),
        "bo_size": 3,
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
def sample_map_1(sample_map_payload_1) -> MatchupMap:
    _map = MatchupMap.from_payload(None, **sample_map_payload_1)
    _map.id = 1
    _map.map_number = 1
    _map.date_created = datetime(2022, 12, 4)
    _map.date_updated = datetime(2022, 12, 4)
    return _map


@pytest.fixture
def sample_map_2(sample_map_payload_2) -> MatchupMap:
    _map = MatchupMap.from_payload(None, **sample_map_payload_2)
    _map.id = 1
    _map.map_number = 2
    _map.date_created = datetime(2022, 12, 7)
    _map.date_updated = datetime(2022, 12, 7)
    return _map


@pytest.fixture
def sample_map_3(sample_map_payload_1) -> MatchupMap:
    _map = MatchupMap.from_payload(None, **sample_map_payload_1)
    _map.id = 3
    _map.map_number = 3
    _map.date_created = datetime(2022, 12, 7)
    _map.date_updated = datetime(2022, 12, 7)
    return _map


@pytest.fixture
def sample_matchup_1(
    sample_matchup_payload: dict,
    sample_team_1: Team,
    sample_team_2: Team,
    sample_map_1: MatchupMap,
) -> Matchup:
    matchup = Matchup(**sample_matchup_payload)
    matchup.id = 1
    matchup.team1 = sample_team_1
    matchup.team2 = sample_team_2
    matchup.maps = [sample_map_1]
    return matchup


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


@pytest.fixture
def sample_matchup_with_global_ban_1(sample_matchup_1: Matchup) -> Matchup:
    sample_matchup_1.with_global_ban = True
    sample_matchup_1.last_no_global_ban = True
    return sample_matchup_1


@pytest.fixture
def sample_matchup_with_global_ban_2(sample_matchup_1: Matchup) -> Matchup:
    sample_matchup_1.with_global_ban = True
    sample_matchup_1.last_no_global_ban = False
    return sample_matchup_1
