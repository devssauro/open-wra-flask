from unittest.mock import patch

from flask import Flask

from app.db_handler.team import PaginatedTeams
from app.mod_auth.models import User
from app.mod_team.models import Team


class TestTeamPost:
    """Test the POST request to Team endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User, sample_team_payload: dict, sample_team_1: Team, sample_app: Flask
    ) -> None:
        """Test if the team was created successfully
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_team_payload(dict): The team payload with the team's data
            sample_team_1(Team): The team object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_team") as cut,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            cut.return_value = sample_team_1
            response = sample_app.post("/v1/team", json=sample_team_payload)
            assert response.status_code == 201
            assert response.json == {"id": 1}

    @staticmethod
    def test_forbidden(sample_team_payload: dict, sample_app: Flask) -> None:
        """Test if the team wasn't created
        Args:
            sample_team_payload(dict): The team payload with the team's data
            sample_app(App): The Flask application
        """
        response = sample_app.post("/v1/team", json=sample_team_payload)
        assert response.status_code == 403


class TestTeamGet:
    """Test the GET request to Team endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User, sample_team_payload: dict, sample_team_1: Team, sample_app: Flask
    ) -> None:
        """Test if the API brings the teams in a list
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_team_payload(dict): The team payload with the team's data
            sample_team_1(Team): The team object returned from DBHandler
            sample_app(App): The Flask application
        """
        with patch("app.db_handler.DBHandler.get_teams") as gt:
            gt.return_value = PaginatedTeams([sample_team_1], 1, 1)
            response = sample_app.get("/v1/team")
            assert response.status_code == 200
            assert response.json["teams"][0]["id"] == 1


class TestTeamPut:
    """Test the PUT request to Team endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User, sample_team_payload: dict, sample_team_1: Team, sample_app: Flask
    ) -> None:
        """Test if the team was updated successfully
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_team_payload(dict): The team payload with the team's data
            sample_team_1(Team): The team object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_team") as cut,
            patch("app.db_handler.DBHandler.get_team_by_id") as gt_id,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            cut.return_value = sample_team_1
            gt_id.return_value = sample_team_1
            response = sample_app.put(f"/v1/team/{sample_team_1.id}", json=sample_team_payload)
            assert response.status_code == 200
            assert response.json == {"msg": "Team has changed"}

    @staticmethod
    def test_not_found(
        sample_admin_user: User, sample_team_payload: dict, sample_app: Flask
    ) -> None:
        """Test if the team wasn't found
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_team_payload(dict): The team payload with the team's data
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_team") as cut,
            patch("app.db_handler.DBHandler.get_team_by_id") as gt_id,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            gt_id.return_value = None
            response = sample_app.put("/v1/team/1", json=sample_team_payload)
            assert response.status_code == 404
            assert response.json == {"msg": "Team not found"}
            assert cut.called is False

    @staticmethod
    def test_forbidden(sample_team_payload: dict, sample_team_1: Team, sample_app: Flask) -> None:
        """Test if the team wasn't created
        Args:
            sample_team_payload(dict): The team payload with the team's data
            sample_app(App): The Flask application
        """
        with patch("app.db_handler.DBHandler.create_update_team") as cut:
            cut.return_value = sample_team_1
            response = sample_app.post("/v1/team", json=sample_team_payload)
            assert response.status_code == 403
