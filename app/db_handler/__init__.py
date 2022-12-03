from app.db_handler.player import PlayerHandler
from app.db_handler.team import TeamHandler


class DBHandler(PlayerHandler, TeamHandler):
    ...
