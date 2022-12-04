from unittest.mock import patch

from flask import Flask

from app.db_handler.matchup import PaginatedMatchups
from app.mod_auth.models import User
from app.mod_tournament.models import Matchup


class TestMatchupPost:
    """Test the POST request to Matchup endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_matchup_payload: dict,
        sample_matchup_1: Matchup,
        sample_app: Flask,
    ) -> None:
        """Test if the matchup was created successfully
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_matchup_payload(dict): The matchup payload with the matchup's data
            sample_matchup_1(Matchup): The matchup object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_matchup") as cum,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            cum.return_value = sample_matchup_1
            response = sample_app.post("/v1/matchup", json=sample_matchup_payload)
            assert response.status_code == 201
            assert response.json == {"id": 1}

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
            sample_admin_user(User): The admin user to be logged in
            sample_matchup_payload(dict): The matchup payload with the matchup's data
            sample_matchup_1(Matchup): The matchup object returned from DBHandler
            sample_app(App): The Flask application
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
