from unittest.mock import patch

from flask import Flask

from app.mod_tournament.models import Champion


class TestChampionGet:
    """Test the GET request to Champion endpoint"""

    @staticmethod
    def test_success(sample_champion_1: Champion, sample_app: Flask) -> None:
        """Test if the API brings the champions in a list
        Args:
            sample_champion_1(Champion): The champion object returned from DBHandler
            sample_app(App): The Flask application
        """
        with patch("app.db_handler.DBHandler.get_champions") as gc:
            gc.return_value = [sample_champion_1]
            response = sample_app.get("/v1/champion")
            assert response.status_code == 200
            assert response.json["champions"][0]["id"] == 1
