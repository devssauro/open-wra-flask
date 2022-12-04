from collections import namedtuple

from app.mod_tournament.models import Tournament, TournamentTeam
from db_config import db

PaginatedTournaments = namedtuple("PaginatedTournaments", ["tournaments", "page", "pages"])


class TournamentHandler:
    """Database handler for Tournament operations"""

    @staticmethod
    def create_update_tournament(tournament: Tournament) -> Tournament:
        """Create or update a tournament
        Args:
            tournament (Tournament): The tournament to be created or updated
        Returns:
            Tournament: The newly created or updated tournament
        """
        db.session.add(tournament)
        db.session.commit()
        return tournament

    @staticmethod
    def create_update_tournament_team(team: TournamentTeam) -> TournamentTeam:
        db.session.add(TournamentTeam)
        db.session.commit()
        return team

    @staticmethod
    def get_tournament_by_id(tournament_id: int) -> Tournament:
        """Get a tournament by id
        Args:
            tournament_id (int): The tournament's id

        Returns:
            Tournament: the tournament object if it exists, else None
        """
        _tournament = Tournament.query.get(tournament_id)
        return _tournament

    @staticmethod
    def get_tournaments(
        name: str | None = None,
        tag: str | None = None,
        region: list[str] | str | None = None,
        female_only: bool | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> PaginatedTournaments:
        """Get a list of tournaments
        Args:
            name (list[int] | int): The tournament's name
            tag (list[int] | int): The tournament's tag
            region (list[str] | str): The tournament's region
            female_only (bool): If the tournament is female only
            page (int): The page for a pagination query, default is 1
            per_page (int): The quantity of teams per page, default is 10

        Returns:
            PaginatedTournaments: The object with all tournaments from that page with the
                current page and the amount of pages available
        """
        args = []
        if name is not None:
            args.append(Tournament.name.contains(name))  # type: ignore
        if tag is not None:
            args.append(Tournament.tag.contains(tag))  # type: ignore
        if region is not None:
            if isinstance(region, str):
                region = [region]
            args.append(Tournament.region.in_(region))  # type: ignore
        if female_only is not None:
            args.append(Tournament.female_only.is_(female_only))  # type: ignore
        query = (
            Tournament.query.filter(*args)
            .order_by(Tournament.name)
            .paginate(page=page, per_page=per_page)
        )

        return PaginatedTournaments(query.items, page, query.pages)
