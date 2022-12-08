from unittest.mock import patch

from flask import Flask


class TestChampionGet:
    """Test the GET request to Patch endpoint"""

    @staticmethod
    def test_success(sample_patch_1: str, sample_app: Flask) -> None:
        """Test if the API brings the patches in a list
        Args:
            sample_patch_1(str): The patch object returned from DBHandler
            sample_app(App): The Flask application
        """
        with patch("app.db_handler.DBHandler.get_patches") as get_patches:
            get_patches.return_value = [sample_patch_1]
            response = sample_app.get("/v1/patch")
            assert response.status_code == 200
            assert response.json["patches"][0] == sample_patch_1
