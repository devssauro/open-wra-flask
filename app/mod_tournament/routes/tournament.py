from flask import Blueprint, request

from app.db_handler import DBHandler
from app.mod_tournament.models import Tournament, TournamentTeam
from db_config import db

bp = Blueprint("tournament", __name__, url_prefix="/tournament")


@bp.get("")
def get_tournaments():
    args = request.args
    result = DBHandler.get_tournaments(
        args.get("name"),
        args.get("tag"),
        args.get("region"),
        args.get("female_only"),
        args.get("page", 1),
        args.get("per_page", 10),
    )

    return {
        "tournaments": [tournament.to_dict() for tournament in result.tournaments],
        "page": result.page,
        "pages": result.pages,
    }


@bp.get("/<int:tournament_id>")
# @roles_accepted("operational", "admin")
def get_tournament_id(tournament_id: int):
    tournament = DBHandler.get_tournament_by_id(tournament_id)
    if not tournament:
        return {"msg": "Tournament not found"}, 404

    return {
        "tournament": {
            **tournament.to_dict(),
            **{
                "lineups": [
                    {
                        "team_id": team.team_id,
                        "entry_phase": team.entry_phase,
                        "players": [p.id for p in team.players],
                    }
                    for team in tournament.teams
                ]
            },
        }
    }


@bp.post("")
# @roles_accepted("operational", "admin")
def post_tournament():
    data = {**request.json}
    if "id" in data:
        del data["id"]
    lineups = []
    if "lineups" in data:
        lineups = data["lineups"]
        del data["lineups"]

    tournament = Tournament.from_payload(None, **data)
    tournament = DBHandler.create_update_tournament(tournament)

    for lineup in lineups:
        players = lineup["players"]
        del lineup["players"]
        team = TournamentTeam(**{**lineup, "tournament_id": tournament.id})
        team.players = DBHandler.get_players_by_ids(players)
        DBHandler.create_update_tournament_team(team)

    return {"tournament_id": tournament.id}, 201


@bp.put("/<int:tournament_id>")
# @roles_accepted("operational", "admin")
def put_tournament(tournament_id: int):
    data = {**request.json}
    if "id" in data:
        del data["id"]
    lineups: list[dict] = []
    if "lineups" in data:
        lineups = data["lineups"]
        del data["lineups"]

    tournament = DBHandler.get_tournament_by_id(tournament_id)
    if tournament is None:
        return {"msg": "Tournament not found"}, 404

    Tournament.from_payload(tournament, **data)

    teams: dict[int, TournamentTeam] = {t.team_id: t for t in tournament.teams}

    for lineup in lineups:
        if lineup["team_id"] in teams.keys():
            teams[lineup["team_id"]].players = DBHandler.get_players_by_ids(lineup["players"])
            teams[lineup["team_id"]].entry_phase = lineup["entry_phase"]
            DBHandler.create_update_tournament_team(teams[lineup["team_id"]])
        else:
            DBHandler.create_update_tournament_team(
                TournamentTeam(**{**lineup, "tournament_id": tournament.id})
            )

    db.session.commit()
    return {"tournament_id": tournament.id}
