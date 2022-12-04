from unittest.mock import patch

from flask import Flask

from app.db_handler.player import PaginatedPlayers
from app.mod_auth.models import User
from app.mod_team.models import Player


class TestPlayerPost:
    """Test the POST request to Player endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_player_payload: dict,
        sample_player_1: Player,
        sample_app: Flask,
    ) -> None:
        """Test if the player was created successfully
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_player_payload(dict): The player payload with the player's data
            sample_player_1(Player): The player object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_player") as cut,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            cut.return_value = sample_player_1
            response = sample_app.post("/v1/player", json=sample_player_payload)
            assert response.status_code == 201
            assert response.json == {"id": 1}

    @staticmethod
    def test_forbidden(sample_player_payload: dict, sample_app: Flask) -> None:
        """Test if the player wasn't created
        Args:
            sample_player_payload(dict): The player payload with the player's data
            sample_app(App): The Flask application
        """
        response = sample_app.post("/v1/player", json=sample_player_payload)
        assert response.status_code == 403


class TestPlayerGet:
    """Test the GET request to Player endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_player_payload: dict,
        sample_player_1: Player,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the players in a list
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_player_payload(dict): The player payload with the player's data
            sample_player_1(Player): The player object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_players") as gt,
            patch("flask_login.utils._get_user") as ge,
        ):
            gt.return_value = PaginatedPlayers([sample_player_1], 1, 1)
            ge.return_value = sample_admin_user
            response = sample_app.get("/v1/player")
            assert response.status_code == 200
            assert response.json["players"][0]["id"] == 1

    @staticmethod
    def test_forbidden(
        sample_player_payload: dict,
        sample_player_1: Player,
        sample_app: Flask,
    ) -> None:
        """Test if the API get an unauthorized access
        Args:
            sample_player_payload(dict): The player payload with the player's data
            sample_player_1(Player): The player object returned from DBHandler
            sample_app(App): The Flask application
        """
        with patch("app.db_handler.DBHandler.get_players") as gt:
            gt.return_value = PaginatedPlayers([sample_player_1], 1, 1)
            response = sample_app.get("/v1/player")
            assert response.status_code == 403


class TestPlayerPut:
    """Test the PUT request to Player endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_player_payload: dict,
        sample_player_1: Player,
        sample_app: Flask,
    ) -> None:
        """Test if the player was updated successfully
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_player_payload(dict): The player payload with the player's data
            sample_player_1(Player): The player object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_player") as cut,
            patch("app.db_handler.DBHandler.get_player_by_id") as gt_id,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            cut.return_value = sample_player_1
            gt_id.return_value = sample_player_1
            response = sample_app.put(
                f"/v1/player/{sample_player_1.id}", json=sample_player_payload
            )
            assert response.status_code == 200
            assert response.json == {"msg": "Player has changed"}

    @staticmethod
    def test_not_found(
        sample_admin_user: User, sample_player_payload: dict, sample_app: Flask
    ) -> None:
        """Test if the player wasn't found
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_player_payload(dict): The player payload with the player's data
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_player") as cut,
            patch("app.db_handler.DBHandler.get_player_by_id") as gt_id,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            gt_id.return_value = None
            response = sample_app.put("/v1/player/1", json=sample_player_payload)
            assert response.status_code == 404
            assert response.json == {"msg": "Player not found"}
            assert cut.called is False

    @staticmethod
    def test_forbidden(
        sample_player_payload: dict, sample_player_1: Player, sample_app: Flask
    ) -> None:
        """Test if the player wasn't created
        Args:
            sample_player_payload(dict): The player payload with the player's data
            sample_app(App): The Flask application
        """
        with patch("app.db_handler.DBHandler.create_update_player") as cut:
            cut.return_value = sample_player_1
            response = sample_app.post("/v1/player", json=sample_player_payload)
            assert response.status_code == 403
