# from app.db_handler import PlayerHandler
# from app.mod_team.models import Player
#
#
# class TestPlayerHandler:
#     @staticmethod
#     def test_create_update_player(sample_app):
#         player = Player(nickname="player", team_id=None, flag="br", role="baron")
#         PlayerHandler.create_update_player(player)
#         assert player.id is not None
#         assert isinstance(player.id, int)
