from collections import namedtuple

from app.mod_team.models import Team
from db_config import db

PaginatedTeams = namedtuple("PaginatedTeams", ["teams", "page", "pages"])


class TeamHandler:
    @staticmethod
    def create_update_team(team: Team) -> Team:
        db.session.add(team)
        db.session.commit()
        return team

    @staticmethod
    def get_team_by_id(team_id: int) -> Team:
        team = db.session.get(team_id)
        return team

    @staticmethod
    def get_teams(tag: str, flag: str, page: int = 1, per_page: int = 10) -> PaginatedTeams:
        args = []
        if tag is not None:
            args.append(Team.tag.contains(tag))  # type: ignore
        if flag is not None:
            args.append(Team.flag.contains(flag))  # type: ignore
        query = Team.query.filter(*args).order_by(Team.nickname).paginate(page, per_page)

        return PaginatedTeams(query.items, page, query.pages)
