from app.db_handler.champion import ChampionHandler
from app.db_handler.patch import PatchHandler
from app.db_handler.player import PlayerHandler
from app.db_handler.team import TeamHandler


class DBHandler(
    ChampionHandler,
    PatchHandler,
    PlayerHandler,
    TeamHandler,
):
    ...
