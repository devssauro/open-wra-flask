# import pytest
# from alembic import command
# from alembic.config import Config
# from decouple import config
#
# from db_config import db
#
#
# @pytest.fixture(autouse=True)
# def create_test_database(sample_app):
#     """Create fresh test database for each test in this package"""
#     c = Config("migrations/alembic.ini")
#     c.set_main_option("script_location", "migrations")
#     c.set_main_option("sqlalchemy.url", config("SQLALCHEMY_DATABASE_TEST_URI"))
#     command.upgrade(c, "head")
#     # db.create_all()
#     yield
#     db.drop_all()
#     # command.downgrade(c, "09952a8b362b")


# @pytest.fixture(autouse=True)
# def create_test_database(sample_app):
#     """Create fresh test database for each test in this package"""
#
#     c = Config("migrations/alembic.ini")
#     c.set_main_option("script_location", "migrations")
#     command.upgrade(c, "head")
#     yield
#     command.downgrade(c, "base")
