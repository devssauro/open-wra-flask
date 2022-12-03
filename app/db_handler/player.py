from collections import namedtuple

from app.mod_team.models import Player
from db_config import db

PaginatedPlayers = namedtuple("PaginatedPlayers", ["players", "page", "pages"])


class PlayerHandler:
    @staticmethod
    def create_update_player(player: Player) -> Player:
        db.session.add(player)
        db.session.commit()
        return player

    @staticmethod
    def get_player_by_id(player_id: int) -> Player:
        player = db.session.get(player_id)
        return player

    @staticmethod
    def get_players(
        nickname: str, region: str, page: int = 1, per_page: int = 10
    ) -> PaginatedPlayers:
        args = []
        if nickname is not None:
            args.append(Player.nickname.contains(nickname))  # type: ignore
        if region is not None:
            args.append(Player.region.contains(region))  # type: ignore
        query = Player.query.filter(*args).order_by(Player.nickname).paginate(page, per_page)

        return PaginatedPlayers(query.items, page, query.pages)
