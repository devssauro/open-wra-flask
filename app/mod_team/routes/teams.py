from flask import Blueprint, request
from flask_security import roles_accepted

from db_config import db

from ...mod_tournament.models import Tournament, TournamentTeam
from ..models import Team

bp = Blueprint("team", __name__, url_prefix="/team")


@bp.get("")
def get_team():
    args = []
    joins = []
    if request.args.get("phase"):
        args.append(Team.phase == request.args["phase"])
    if request.args.get("t"):
        joins.append((TournamentTeam, TournamentTeam.team_id == Team.id))
        joins.append((Tournament, Tournament.id == TournamentTeam.tournament_id))
        args.append(Tournament.id.in_(request.args.getlist("t")))
    sort = Team.tag if request.args.get("sort") == "tag" else Team.name
    if len(joins):
        teams = (
            Team.query.with_entities(
                Team.id,
                Team.flag,
                Team.name,
                Team.phase,
                Team.tag,
            )
            .outerjoin(*joins)
            .filter(*args)
            .order_by(sort)
        )
    else:
        teams = (
            Team.query.with_entities(
                Team.id,
                Team.flag,
                Team.name,
                Team.phase,
                Team.tag,
            )
            .filter(*args)
            .order_by(sort)
        )

    return {
        "teams": [
            dict(
                id=team.id,
                flag=team.flag,
                name=team.name,
                phase=team.phase,
                tag=team.tag,
                label=f"{team.tag} - {team.name}",
            )
            for team in teams
        ]
    }


@bp.post("")
@roles_accepted("operational", "admin")
def post_team():
    if "id" in request.json:
        del request.json["id"]
    team: Team = Team(**request.json)
    db.session.add(team)
    db.session.commit()

    return {"id": team.id}, 201


@bp.put("")
@roles_accepted("operational", "admin")
def put_team():
    if "id" not in request.json:
        return {"msg": "id is missing"}

    team: Team = Team.query.get(request.json["id"])
    team.name = request.json["name"]
    team.tag = request.json["tag"]
    team.flag = request.json["flag"]
    db.session.add(team)
    db.session.commit()

    return {"msg": "Team has changed"}
