from collections import namedtuple

from app.mod_team.models import Team
from db_config import db

PaginatedTeams = namedtuple("PaginatedTeams", ["teams", "page", "pages"])


class TeamHandler:
    """Database handler for Team operations"""

    @staticmethod
    def create_update_team(team: Team) -> Team:
        """Create or update a team
        Args:
            team (Team): The team to be created or updated
        Returns:
            Team: The newly created or updated team
        """
        db.session.add(team)
        db.session.commit()
        return team

    @staticmethod
    def get_team_by_id(team_id: int) -> Team:
        """Get a team by id
        Args:
            team_id (int): The team's id

        Returns:
            Team: the team object if it exists, else None
        """
        team = db.session.get(team_id)
        return team

    @staticmethod
    def get_teams(tag: str, flag: str, page: int = 1, per_page: int = 10) -> PaginatedTeams:
        """Get a list of teams
        Args:
            tag (str): The team's tag
            flag (str): The team's region
            page (int): The page for a pagination query, default is 1
            per_page (int): The quantity of teams per page, default is 10

        Returns:
            PaginatedTeams: The object with all teams from that page with the
                current page and the amount of pages available
        """
        args = []
        if tag is not None:
            args.append(Team.tag.contains(tag))  # type: ignore
        if flag is not None:
            args.append(Team.flag.contains(flag))  # type: ignore
        query = Team.query.filter(*args).order_by(Team.nickname).paginate(page, per_page)

        return PaginatedTeams(query.items, page, query.pages)
