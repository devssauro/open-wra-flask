import pytest


@pytest.fixture
def sample_picks_bans_payload() -> dict:
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
    return {**sample_picks_bans_payload, "blue_ban_1": 2}


@pytest.fixture
def sample_draft_payload(sample_picks_bans_payload: dict) -> dict:
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
    return {
        **sample_players_payload,
        "blue_baron_player": sample_players_payload["blue_jungle_player"],
    }
