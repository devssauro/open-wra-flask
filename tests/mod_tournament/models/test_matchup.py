import pytest

from app.exceptions import GlobalBanError
from app.mod_tournament.models import Matchup, MatchupMap


class TestMatchup:
    """Tests made to ensure the matchup add_map works properly"""

    @staticmethod
    def test_success(
        sample_matchup_with_global_ban_1: Matchup,
        sample_map_2: MatchupMap,
    ) -> None:
        assert sample_matchup_with_global_ban_1.add_map(sample_map_2)

    @staticmethod
    def test_second_map_error(
        sample_matchup_with_global_ban_1: Matchup,
        sample_map_1: MatchupMap,
    ) -> None:
        with pytest.raises(GlobalBanError):
            assert sample_matchup_with_global_ban_1.add_map(sample_map_1)

    @staticmethod
    def test_second_map_without_global_ban_success(
        sample_matchup_1: Matchup,
        sample_map_1: MatchupMap,
    ) -> None:
        assert sample_matchup_1.add_map(sample_map_1)

    @staticmethod
    def test_last_map_lngb_success(
        sample_matchup_with_global_ban_1: Matchup,
        sample_map_3: MatchupMap,
    ) -> None:
        assert sample_matchup_with_global_ban_1.add_map(sample_map_3)

    @staticmethod
    def test_last_map_without_lngb_error(
        sample_matchup_with_global_ban_2: Matchup,
        sample_map_3: MatchupMap,
    ) -> None:
        with pytest.raises(GlobalBanError):
            assert sample_matchup_with_global_ban_2.add_map(sample_map_3)
