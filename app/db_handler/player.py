from collections import namedtuple

from app.mod_team.models import Player
from db_config import db

PaginatedPlayers = namedtuple("PaginatedPlayers", ["players", "page", "pages"])


class PlayerHandler:
    """Database handler for Player operations"""

    @staticmethod
    def create_update_player(player: Player) -> Player:
        """Create or update a player
        Args:
            player (Player): The player to be created or updated
        Returns:
            Player: The newly created or updated player
        """
        db.session.add(player)
        db.session.commit()
        return player

    @staticmethod
    def get_player_by_id(player_id: int) -> Player:
        """Get a player by id
        Args:
            player_id (int): The player's id

        Returns:
            Player: the player object if it exists, else None
        """
        player = db.session.get(player_id)
        return player

    @staticmethod
    def get_players_by_ids(players_ids: list[int]) -> list[Player]:
        """Get a list of players by a list of ids
        Args:
            players_ids (int): The player's ids

        Returns:
            list[Player]: the list of players based on ids
        """
        return list(Player.query.filter(Player.id.in_(players_ids)))  # type: ignore

    @staticmethod
    def get_players(
        nickname: str, region: str, page: int = 1, per_page: int = 10
    ) -> PaginatedPlayers:
        """Get a list of players
        Args:
            nickname (str): The player's nickname
            region (str): The player's region
            page (int): The page for a pagination query, default is 1
            per_page (int): The quantity of teams per page, default is 10

        Returns:
            PaginatedPlayers: The object with all players from that page with the
                current page and the amount of pages available
        """
        args = []
        if nickname is not None:
            args.append(Player.nickname.contains(nickname))  # type: ignore
        if region is not None:
            args.append(Player.region.contains(region))  # type: ignore
        query = (
            Player.query.filter(*args)
            .order_by(Player.nickname)
            .paginate(page=page, per_page=per_page)
        )

        return PaginatedPlayers(query.items, page, query.pages)
