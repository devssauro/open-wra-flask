from unittest.mock import patch

from flask import Flask

from app.db_handler.tournament import PaginatedTournaments
from app.mod_auth.models import User
from app.mod_tournament.models import Tournament, TournamentTeam


class TestTournamentPost:
    """Test the POST request to Tournament endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_tournament_payload_1,
        sample_tournament_1: Tournament,
        sample_tournament_team_1: TournamentTeam,
        sample_app: Flask,
    ) -> None:
        """Test if the tournament was created successfully
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_tournament_payload_1 (dict): The tournament payload with the tournament's data
            sample_tournament_1 (Tournament): The tournament object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_tournament") as create_update_tournament,
            patch(
                "app.db_handler.DBHandler.create_update_tournament_team"
            ) as create_update_tournament_team,
            patch("flask_login.utils._get_user") as _get_user,
        ):
            _get_user.return_value = sample_admin_user
            create_update_tournament.return_value = sample_tournament_1
            create_update_tournament_team.return_value = sample_tournament_team_1
            response = sample_app.post("/v1/tournament", json=sample_tournament_payload_1)
            assert response.status_code == 201
            assert response.json == {"tournament_id": 1}

    @staticmethod
    def test_forbidden(sample_tournament_payload_1, sample_app: Flask) -> None:
        """Test if the tournament wasn't created
        Args:
            sample_tournament_payload_1 (dict): The tournament payload with the tournament's data
            sample_app (App): The Flask application
        """
        response = sample_app.post("/v1/tournament", json=sample_tournament_payload_1)
        assert response.status_code == 403


class TestTournamentGet:
    """Test the GET request to Tournament endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_tournament_1: Tournament,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the tournaments in a list
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_tournament_1 (Tournament): The tournament object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_tournaments") as get_tournaments,
            patch("flask_login.utils._get_user") as _get_user,
        ):
            get_tournaments.return_value = PaginatedTournaments([sample_tournament_1], 1, 1)
            _get_user.return_value = sample_admin_user
            response = sample_app.get("/v1/tournament")
            assert response.status_code == 200
            assert response.json["tournaments"][0]["id"] == 1


class TestTournamentGetById:
    """Test the GET request to Tournament endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_tournament_1: Tournament,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the tournaments object
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_tournament_1 (Tournament): The tournament object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_tournament_by_id") as get_tournament_by_id,
            patch("flask_login.utils._get_user") as _get_user,
        ):
            get_tournament_by_id.return_value = sample_tournament_1
            _get_user.return_value = sample_admin_user
            response = sample_app.get(f"/v1/tournament/{sample_tournament_1.id}")
            assert response.status_code == 200
            assert response.json["tournament"]["id"] == 1

    @staticmethod
    def test_not_found(
        sample_admin_user: User,
        sample_app: Flask,
    ) -> None:
        """Test if the API doesn't found the tournament
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_tournament_by_id") as get_tournament_by_id,
            patch("flask_login.utils._get_user") as _get_user,
        ):
            get_tournament_by_id.return_value = None
            _get_user.return_value = sample_admin_user
            response = sample_app.get("/v1/tournament/1")
            assert response.status_code == 404
            assert response.json == {"msg": "Tournament not found"}


class TestTournamentPut:
    """Test the PUT request to Tournament endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_tournament_payload_1,
        sample_tournament_1: Tournament,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the tournaments in a list
        Args:
            sample_admin_user (User): The admin user to be logged in
            sample_tournament_payload_1 (dict): The tournament payload
            sample_tournament_1 (Tournament): The tournament object returned from DBHandler
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_tournament") as create_update_tournament,
            patch("app.db_handler.DBHandler.get_tournament_by_id") as get_tournament_by_id,
            patch("flask_login.utils._get_user") as _get_user,
        ):
            get_tournament_by_id.return_value = sample_tournament_1
            _get_user.return_value = sample_admin_user
            create_update_tournament.return_value = sample_tournament_1
            response = sample_app.put(
                f"/v1/tournament/{sample_tournament_1.id}", json=sample_tournament_payload_1
            )
            assert response.status_code == 200
            assert response.json == {"tournament_id": 1}

    @staticmethod
    def test_not_found(
        sample_admin_user: User,
        sample_tournament_payload_1,
        sample_app: Flask,
    ) -> None:
        """Test if the API gets nof found
        Args:
            sample_tournament_payload_1 (dict): The tournament payload
            sample_admin_user (User): The admin user to be logged in
            sample_app (App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_tournament_by_id") as get_tournament_by_id,
            patch("flask_login.utils._get_user") as _get_user,
        ):
            get_tournament_by_id.return_value = None
            _get_user.return_value = sample_admin_user
            response = sample_app.put("/v1/tournament/1", json=sample_tournament_payload_1)
            assert response.status_code == 404
            assert response.json == {"msg": "Tournament not found"}

    @staticmethod
    def test_forbidden(sample_tournament_payload_1, sample_app: Flask) -> None:
        """Test if the user has no permission
        Args:
            sample_tournament_payload_1(dict): The tournament payload
            sample_app(App): The Flask application
        """
        response = sample_app.put("/v1/tournament/1", json=sample_tournament_payload_1)
        assert response.status_code == 403
