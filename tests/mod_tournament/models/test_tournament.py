from app.mod_tournament.models import Tournament


class TestTournament:
    """Tests made to ensure the tournament is correctly filled"""

    @staticmethod
    def test_with_string(sample_tournament_payload_1: dict) -> None:
        """Check if the picks and bans are correctly set"""
        pb = Tournament.from_payload(None, **sample_tournament_payload_1)
        assert isinstance(pb, Tournament)
        assert pb.phases == ["group", "playoffs", "final"]

    @staticmethod
    def test_with_dict_list(sample_tournament_payload_2: dict) -> None:
        """Check if the picks and bans are correctly set"""
        pb = Tournament.from_payload(None, **sample_tournament_payload_2)
        assert isinstance(pb, Tournament)
        assert pb.phases == ["group", "quarterfinals", "semifinals", "final"]

    @staticmethod
    def test_with_string_list(sample_tournament_payload_3: dict) -> None:
        """Check if the picks and bans are correctly set"""
        pb = Tournament.from_payload(None, **sample_tournament_payload_3)
        assert isinstance(pb, Tournament)
        assert pb.phases == ["group", "knockout", "final"]
