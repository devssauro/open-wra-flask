from collections import namedtuple

from app.mod_tournament.models import MatchupMap
from db_config import db

PaginatedMatchupMaps = namedtuple("PaginatedMatchupMaps", ["maps", "page", "pages"])


class MatchupMapHandler:
    """Database handler for MatchupMap operations"""

    @staticmethod
    def create_update_map(map: MatchupMap) -> MatchupMap:
        """Create or update a map
        Args:
            map (MatchupMap): The map to be created or updated
        Returns:
            MatchupMap: The newly created or updated map
        """
        db.session.add(map)
        db.session.commit()
        return map

    @staticmethod
    def get_map_by_id(map_id: int) -> MatchupMap:
        """Get a map by id
        Args:
            map_id (int): The map's id

        Returns:
            MatchupMap: the map object if it exists, else None
        """
        _map = MatchupMap.query.get(map_id)
        return _map

    @staticmethod
    def get_maps(
        tournament: list[int] | int | None = None,
        matchup: list[int] | int | None = None,
        patch: list[str] | str | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> PaginatedMatchupMaps:
        """Get a list of maps
        Args:
            tournament (list[int] | int): The tournament id to be filtered
            matchup (list[int] | int): The matchups to be filtered
            patch (list[str] | str): The patches to be filtered
            page (int): The page for a pagination query, default is 1
            per_page (int): The quantity of teams per page, default is 10

        Returns:
            PaginatedMatchupMaps: The object with all maps from that page with the
                current page and the amount of pages available
        """
        args = []
        if tournament is not None:
            if isinstance(tournament, int):
                tournament = [tournament]
            args.append(MatchupMap.tournament_id.in_(tournament))
        if matchup is not None:
            if isinstance(matchup, int):
                matchup = [matchup]
            args.append(MatchupMap.matchup_id.in_(matchup))
        if patch is not None:
            if isinstance(patch, int):
                patch = [patch]
            args.append(MatchupMap.patch.in_(patch))
        query = (
            MatchupMap.query.filter(*args)
            .order_by(MatchupMap.matchup_id, MatchupMap.map_number)
            .paginate(page, per_page)
        )

        return PaginatedMatchupMaps(query.items, page, query.pages)
