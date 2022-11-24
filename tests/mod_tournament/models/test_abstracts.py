import pytest

from app.exceptions import DraftIntegrityError, LineupIntegrityError
from app.mod_tournament.models.abstracts import Draft, PicksBans, Players


class TestPicksBans:
    """Tests made to ensure the integrity check on Picks & Bans"""

    @staticmethod
    def test_success(sample_picks_bans_payload: dict) -> None:
        """Check if the picks and bans are correctly set"""
        pb = PicksBans.from_payload(None, **sample_picks_bans_payload)
        assert isinstance(pb, PicksBans)

    @staticmethod
    def test_draft_error(sample_wrong_picks_bans_payload: dict) -> None:
        """Check if the method raises the failure on picks and bans integrity"""
        with pytest.raises(DraftIntegrityError):
            PicksBans.from_payload(None, **sample_wrong_picks_bans_payload)


class TestDraft:
    """Tests made to ensure the integrity check on Blue & Red drafts"""

    @staticmethod
    def test_success(sample_draft_payload: dict):
        """Check if the draft is correctly set"""
        draft = Draft.from_payload(None, **sample_draft_payload)
        assert isinstance(draft, Draft)

    @staticmethod
    def test_blue_draft_error(sample_wrong_blue_draft_payload: dict):
        """Check if the method raises the failure on blue side draft integrity"""
        with pytest.raises(DraftIntegrityError):
            Draft.from_payload(None, **sample_wrong_blue_draft_payload)

    @staticmethod
    def test_red_draft_error(sample_wrong_red_draft_payload: dict):
        """Check if the method raises the failure on red side draft integrity"""
        with pytest.raises(DraftIntegrityError):
            Draft.from_payload(None, **sample_wrong_red_draft_payload)


class TestPlayes:
    """Tests made to ensure the integrity check on Players positions"""

    @staticmethod
    def test_success(sample_players_payload: dict) -> None:
        """Check if the picks and bans are correctly set"""
        players = Players.from_payload(None, **sample_players_payload)
        assert isinstance(players, Players)

    @staticmethod
    def test_error(sample_wrong_players_payload: dict) -> None:
        """Check if the method raises the failure on player position integrity"""
        with pytest.raises(LineupIntegrityError):
            Players.from_payload(None, **sample_wrong_players_payload)
