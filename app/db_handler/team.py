from collections import namedtuple

from app.mod_team.models import Team
from db_config import db

PaginatedTeams = namedtuple("PaginatedTeams", ["teams", "page", "pages"])
LineupTeam = namedtuple("LineupTeam", ["team", "players"])


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
        team = Team.query.get(team_id)
        return team

    @staticmethod
    def get_teams_from_matchup(
        tournament_id: int,
        teams_ids: tuple[int] | list[int],
    ) -> list[LineupTeam]:
        """Get the teams from a matchup
        Args:
            tournament_id (int): The tournament's id from matchup
            teams_ids (tuple[int] | list[int]): The team's IDs from matchup

        Returns:
            list[Team]: The teams from a Matchup
        """
        teams = Team.query.filter(Team.id.in_(teams_ids))  # type: ignore
        return [
            LineupTeam(
                team,
                *[
                    lineup.players
                    for lineup in team.lineups
                    if lineup.tournament_id == tournament_id
                ],
            )
            for team in teams
        ]

    @staticmethod
    def get_teams(
        tag: str | None, flag: str | None, order_by: str = "tag", page: int = 1, per_page: int = 10
    ) -> PaginatedTeams:
        """Get a list of teams
        Args:
            tag (str): The team's tag
            flag (str): The team's region
            order_by (str): How to order teams, by tag or by name
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
        query = (
            Team.query.filter(*args).order_by(Team.tag if order_by == "tag" else Team.name)
            # .paginate(page=page, per_page=per_page, error_out=False)
        )

        return PaginatedTeams(query, page, 10)
