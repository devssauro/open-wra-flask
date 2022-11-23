from typing import Dict, List

from flask import Blueprint, request
from flask_security import roles_accepted

from db_config import db

from ...mod_team.models import Player
from ..models import Tournament, TournamentTeam

bp = Blueprint("tournament", __name__, url_prefix="/tournament")


@bp.get("")
def get_tournaments():
    args = []
    if request.args.get("s"):
        args.append(Tournament.name.contains(request.args["s"]))
    if "female_only" in request.args and request.args["female_only"] is not False:
        args.append(Tournament.female_only)
    tournaments: Tournament = Tournament.query.filter(*args).order_by(Tournament.name)

    return {"tournaments": [tournament.to_dict() for tournament in tournaments]}


@bp.get("/<int:id>")
@roles_accepted("operational", "admin")
def get_tournament_id(id: int):
    tournament: Tournament = Tournament.query.get(id)
    teams: TournamentTeam = TournamentTeam.query.filter(
        TournamentTeam.tournament_id == tournament.id
    )
    return {
        "tournament": {
            "id": tournament.id,
            "tag": tournament.tag,
            "region": tournament.region,
            "split": tournament.split,
            "phases": tournament.phases,
            "female_only": tournament.female_only,
            "lineups": [
                {
                    "team_id": team.team_id,
                    "entry_phase": team.entry_phase,
                    "players": [p.id for p in team.players],
                }
                for team in teams
            ],
        }
    }


@bp.post("")
@roles_accepted("operational", "admin")
def post_tournament():
    data = {**request.json}
    if "id" in data:
        del data["id"]
    lineups: List[Dict] = []
    if "lineups" in data:
        lineups = data["lineups"]
        del data["lineups"]
    tournament: Tournament = Tournament(**data)
    db.session.add(tournament)
    db.session.commit()

    for lineup in lineups:
        players = lineup["players"]
        del lineup["players"]
        t_team: TournamentTeam = TournamentTeam(**{**lineup, "tournament_id": tournament.id})
        db.session.add(t_team)
        db.session.commit()
        for player in players:
            t_team.players.append(Player.query.get(player))

    db.session.commit()
    return {"tournament": tournament.id}


@bp.put("")
@roles_accepted("operational", "admin")
def put_tournament():
    data = {**request.json}
    _id = None
    if "id" in data:
        _id = data["id"]
        del data["id"]
    lineups: List[Dict] = []
    if "lineups" in data:
        lineups = data["lineups"]
        del data["lineups"]

    tournament: Tournament | None = None
    if _id is None:
        tournament: Tournament = Tournament(**data)
        db.session.add(tournament)
        db.session.commit()

        for lineup in lineups:
            players = lineup["players"]
            del lineup["players"]
            t_team = TournamentTeam(**{**lineup, "tournament_id": tournament.id})
            db.session.add(t_team)
            db.session.commit()
            for player in players:
                t_team.players.append(Player.query.get(player))
    else:
        tournament: Tournament = Tournament.query.get(_id)
        teams: Dict[int, TournamentTeam] = {
            t.team_id: t for t in TournamentTeam.query.filter(TournamentTeam.tournament_id == _id)
        }
        for lineup in lineups:
            if lineup["team_id"] in teams.keys():
                teams[lineup["team_id"]].players = list(
                    Player.query.filter(Player.id.in_(lineup["players"]))
                )
                teams[lineup["team_id"]].entry_phase = lineup["entry_phase"]
            else:
                t_team = TournamentTeam(**{**lineup, "tournament_id": tournament.id})
                db.session.add(t_team)

    db.session.commit()
    return {"tournament": tournament.id}
