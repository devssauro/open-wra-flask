from unittest.mock import patch

from flask import Flask

from app.mod_auth.models import User
from app.mod_tournament.models import Matchup, MatchupMap


class TestMatchupMapPost:
    """Test the POST request to MatchupMap endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_map_payload: dict,
        sample_map_1: MatchupMap,
        sample_matchup_1: Matchup,
        sample_app: Flask,
    ) -> None:
        """Test if the map was created successfully
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_map_payload(dict): The map payload with the map's data
            sample_map_1(MatchupMap): The map object returned from DBHandler
            sample_matchup_1(Matchup): The matchup to be linked to map
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_map") as cum,
            patch("app.db_handler.DBHandler.get_matchup_by_id") as gm_bi,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            cum.return_value = sample_map_1
            gm_bi.return_value = sample_matchup_1
            response = sample_app.post("/v1/matchup/1/map", json=sample_map_payload)
            assert response.status_code == 201
            assert response.json == {"map_id": 1}

    @staticmethod
    def test_not_found(
        sample_admin_user: User,
        sample_map_payload: dict,
        sample_app: Flask,
    ) -> None:
        """Test if the matchup is not found
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_map_payload(dict): The map payload with the map's data
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_map") as cum,
            patch("app.db_handler.DBHandler.get_matchup_by_id") as gm_bi,
            patch("flask_login.utils._get_user") as ge,
        ):
            ge.return_value = sample_admin_user
            gm_bi.return_value = None
            response = sample_app.post("/v1/matchup/1/map", json=sample_map_payload)
            assert response.status_code == 404
            assert response.json == {"msg": "Matchup not found"}
            assert cum.called is False

    @staticmethod
    def test_forbidden(sample_map_payload: dict, sample_app: Flask) -> None:
        """Test if the map wasn't created
        Args:
            sample_map_payload(dict): The map payload with the map's data
            sample_app(App): The Flask application
        """
        response = sample_app.post("/v1/matchup/1/map", json=sample_map_payload)
        assert response.status_code == 403


class TestMatchupMapGet:
    """Test the GET request to MatchupMap endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_map_1: MatchupMap,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the maps in a list
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_map_1(MatchupMap): The map object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_map_by_id") as gm,
            patch("flask_login.utils._get_user") as ge,
        ):
            gm.return_value = sample_map_1
            ge.return_value = sample_admin_user
            response = sample_app.get(f"/v1/matchup/1/map/{sample_map_1.id}/edit")
            assert response.status_code == 200
            assert response.json["id"] == 1

    @staticmethod
    def test_not_found(
        sample_admin_user: User,
        sample_app: Flask,
    ) -> None:
        """Test if the API gets nof found
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_map_by_id") as gm,
            patch("flask_login.utils._get_user") as ge,
        ):
            gm.return_value = None
            ge.return_value = sample_admin_user
            response = sample_app.get("/v1/matchup/1/map/1/edit")
            assert response.status_code == 404
            assert response.json == {"msg": "Map not found"}

    @staticmethod
    def test_forbidden(sample_app: Flask) -> None:
        """Test if the user has no permission
        Args:
            sample_app(App): The Flask application
        """
        response = sample_app.get("/v1/matchup/1/map/1/edit")
        assert response.status_code == 403


class TestMatchupMapPut:
    """Test the PUT request to MatchupMap endpoint"""

    @staticmethod
    def test_success(
        sample_admin_user: User,
        sample_map_payload: dict,
        sample_map_1: MatchupMap,
        sample_app: Flask,
    ) -> None:
        """Test if the API brings the maps in a list
        Args:
            sample_admin_user(User): The admin user to be logged in
            sample_map_payload(dict): The map payload
            sample_map_1(MatchupMap): The map object returned from DBHandler
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.create_update_map") as cum,
            patch("app.db_handler.DBHandler.get_map_by_id") as gm,
            patch("flask_login.utils._get_user") as ge,
        ):
            gm.return_value = sample_map_1
            ge.return_value = sample_admin_user
            cum.return_value = sample_map_1
            response = sample_app.put(
                f"/v1/matchup/1/map/{sample_map_1.id}/edit", json=sample_map_payload
            )
            assert response.status_code == 200
            assert response.json["id"] == 1

    @staticmethod
    def test_not_found(
        sample_admin_user: User,
        sample_map_payload: dict,
        sample_app: Flask,
    ) -> None:
        """Test if the API gets nof found
        Args:
            sample_map_payload(dict): The map payload
            sample_admin_user(User): The admin user to be logged in
            sample_app(App): The Flask application
        """
        with (
            patch("app.db_handler.DBHandler.get_map_by_id") as gm,
            patch("flask_login.utils._get_user") as ge,
        ):
            gm.return_value = None
            ge.return_value = sample_admin_user
            response = sample_app.put("/v1/matchup/1/map/1/edit", json=sample_map_payload)
            assert response.status_code == 404
            assert response.json == {"msg": "Map not found"}

    @staticmethod
    def test_forbidden(sample_map_payload: dict, sample_app: Flask) -> None:
        """Test if the user has no permission
        Args:
            sample_map_payload(dict): The map payload
            sample_app(App): The Flask application
        """
        response = sample_app.put("/v1/matchup/1/map/1/edit", json=sample_map_payload)
        assert response.status_code == 403
