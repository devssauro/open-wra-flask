from typing import List

from flask import Blueprint, request
from flask_security import roles_accepted

from app.db_handler import DBHandler
from app.db_handler.matchup import PaginatedMatchups
from app.mod_team.models import Team
from app.mod_tournament.models import Matchup, Tournament, TournamentTeam

bp = Blueprint("matchup", __name__, url_prefix="/matchup")


@bp.get("")
def get_matchups():
    args = request.args
    result: PaginatedMatchups = DBHandler.get_matchups(
        tournament=args.getlist("tournament"),
        page=args.get("page", 1),
        per_page=args.get("per_page", 10),
    )
    return {
        "matchups": [
            {
                "id": matchup.id,
                "phase": matchup.phase,
                "datetime": matchup.datetime.isoformat(),
                "team1": {
                    "id": matchup.team1.id,
                    "tag": matchup.team1.tag,
                    "name": matchup.team1.name,
                },
                "team2": {
                    "id": matchup.team2.id,
                    "tag": matchup.team2.tag,
                    "name": matchup.team2.name,
                },
                "maps": [
                    {
                        "id": map.id,
                        "winner": "team1" if map.winner == matchup.team1_id else "team2",
                        "winner_side": map.winner_side,
                        "length": map.length,
                        "vod_link": map.vod_link,
                    }
                    for map in [m for m in matchup.maps if m.matchup_id == matchup.id]
                ],
            }
            for matchup in result.matchups
        ],
        "page": result.page,
        "pages": result.pages,
    }


@bp.get("/<int:matchup_id>/teams")
def get_matchup_teams(matchup_id: int):
    matchup: List[TournamentTeam] = list(
        TournamentTeam.query.outerjoin(
            (Tournament, Tournament.id == TournamentTeam.tournament_id),
            (Matchup, Matchup.tournament_id == Tournament.id),
        ).filter(
            Matchup.id == matchup_id,
            TournamentTeam.team_id.in_([Matchup.team1_id, Matchup.team2_id]),  # type: ignore
        )
    )
    teams = Team.query.filter(Team.id.in_([t.team_id for t in matchup]))  # type: ignore

    return {
        "id": matchup_id,
        **{
            f"team{team[0]+1}": {
                "name": [t.name for t in teams if t.id == team[1].team_id][0],
                "id": team[1].team_id,
                "players": [
                    player.to_dict(only=("id", "nickname", "role")) for player in team[1].players
                ],
            }
            for team in enumerate(matchup)
        },
    }


@bp.post("")
@roles_accepted("operational", "admin")
def post_matchup():
    matchup = Matchup(**request.json)
    matchup = DBHandler.create_update_matchup(matchup)

    return {"id": matchup.id}, 201
