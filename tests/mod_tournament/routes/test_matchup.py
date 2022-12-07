from unittest.mock import patch

from flask import Flask

from app.db_handler.matchup import PaginatedMatchups
from app.db_handler.team import LineupTeam
from app.mod_auth.models import User
from app.mod_tournament.models import Matchup, Tournament


class TestMatchupPost:
    """Test the POST request to Matchup endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_matchup_payload: dict,
        sample_matchup_1: Matchup,
        sample_tournament_2: Tournament,
        sample_app: Flask,
    ) -> None:
        """Test if the matchup was created successfully
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_matchup_payload (dict): The matchup payload with the matchup's data
            sample_matchup_1 (Matchup): The matchup object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_matchup") as cum,
            patch("app.db_handler.DBHandler.get_tournament_by_id") as gt_bi,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            gt_bi.return_value = sample_tournament_2
            cum.return_value = sample_matchup_1
            response = sample_app.post("/v1/matchup", json=sample_matchup_payload)
            assert response.status_code == 201
            assert response.json == {"id": 1}

    @staticmethod
    def test_not_found(
        sample_admin_user: User,
        sample_matchup_payload: dict,
        sample_matchup_1: Matchup,
        sample_app: Flask,
    ) -> None:
        """Test if the matchup was created successfully
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_matchup_payload (dict): The matchup payload with the matchup's data
            sample_matchup_1 (Matchup): The matchup object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_matchup") as cum,
            patch("app.db_handler.DBHandler.get_tournament_by_id") as gt_bi,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            gt_bi.return_value = None
            cum.return_value = sample_matchup_1
            response = sample_app.post("/v1/matchup", json=sample_matchup_payload)
            assert response.status_code == 404
            assert response.json == {"msg": "Tournament not found"}

    @staticmethod
    def test_forbidden(sample_matchup_payload: dict, sample_app: Flask) -> None:
        """Test if the matchup wasn't created
        Args:
            sample_matchup_payload(dict): The matchup payload with the matchup's data
            sample_app(App): The Flask application
        """
        response = sample_app.post("/v1/matchup", json=sample_matchup_payload)
        assert response.status_code == 403


class TestMatchupGet:
    """Test the GET request to Matchup endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_matchup_payload: dict,
        sample_matchup_1: Matchup,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the matchups in a list
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_matchup_payload (dict): The matchup payload with the matchup's data
            sample_matchup_1 (Matchup): The matchup object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_matchups") as gm,
            patch("flask_login.utils._get_user") as ge,
        ):
            gm.return_value = PaginatedMatchups([sample_matchup_1], 1, 1)
            ge.return_value = sample_admin_user
            response = sample_app.get("/v1/matchup")
            assert response.status_code == 200
            assert response.json["matchups"][0]["id"] == 1


class TestMatchupTeamGet:
    """Test the GET request to Teams from Matchup endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_matchup_payload: dict,
        sample_matchup_1: Matchup,
        sample_app: Flask,
        sample_lieneupteam_list_sample: list[LineupTeam],
    ) -> None:
        """Test if the API brings the matchups in a list
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_matchup_payload (dict): The matchup payload with the matchup's data
            sample_matchup_1 (Matchup): The matchup object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_teams_from_matchup") as gt_fm,
            patch("flask_login.utils._get_user") as ge,
        ):
            gt_fm.return_value = sample_lieneupteam_list_sample
            ge.return_value = sample_admin_user
            response = sample_app.get(f"/v1/matchup/{sample_matchup_1.id}/teams")
            assert response.status_code == 200
            assert response.json["id"] == 1

    @staticmethod
    def test_not_found(sample_admin_user: User, sample_app: Flask) -> None:
        """Test if the API brings the matchups in a list
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_teams_from_matchup") as gt_fm,
            patch("app.db_handler.DBHandler.get_matchup_by_id") as gm_bi,
            patch("flask_login.utils._get_user") as ge,
        ):
            gm_bi.return_value = None
            ge.return_value = sample_admin_user
            response = sample_app.get("/v1/matchup/1/teams")
            assert response.status_code == 404
            assert gt_fm.called is False

    @staticmethod
    def test_forbidden(sample_app: Flask) -> None:
        """Test if the API brings the matchups in a list
        Args:
            sample_app(App): The Flask application
        """
        response = sample_app.get("/v1/matchup/1/teams")
        assert response.status_code == 403
