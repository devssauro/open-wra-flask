from collections import namedtuple

from app.mod_tournament.models import Matchup
from db_config import db

PaginatedMatchups = namedtuple("PaginatedMatchups", ["matchups", "page", "pages"])


class MatchupHandler:
    """Database handler for Matchup operations"""

    @staticmethod
    def create_update_matchup(matchup: Matchup) -> Matchup:
        """Create or update a matchup
        Args:
            matchup (Matchup): The matchup to be created or updated
        Returns:
            Matchup: The newly created or updated matchup
        """
        db.session.add(matchup)
        db.session.commit()
        return matchup

    @staticmethod
    def get_matchup_by_id(matchup_id: int) -> Matchup:
        """Get a matchup by id
        Args:
            matchup_id (int): The matchup's id

        Returns:
            Matchup: the Matchup object if it exists, else None
        """
        matchup = Matchup.query.get(matchup_id)
        return matchup

    @staticmethod
    def get_matchups(
        tournament: list[int] | int | None = None,
        page: int = 1,
        per_page: int = 1,
    ) -> PaginatedMatchups:
        """Get a list of Matchups
        Args:
            tournament (list[int] | int): The tournaments to be filtered
            page (int): The page for a pagination query, default is 1
            per_page (int):The quantity of matchups per page, default is 10

        Returns:
            PaginatedMatchups: The object with all matchups from that page with the
                current page and the amount of pages available
        """
        args = []
        if tournament is not None:
            if isinstance(tournament, int):
                tournament = [tournament]
            args.append(Matchup.tournament_id.in_(tournament))  # type: ignore
        query = (
            Matchup.query.filter(*args)
            .order_by(Matchup.datetime.desc())
            .paginate(page=page, per_page=per_page)
        )

        return PaginatedMatchups(matchups=query.items, page=page, pages=query.pages)
