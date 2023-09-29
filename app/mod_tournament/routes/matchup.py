from flask import Blueprint, request

from app.db_handler import DBHandler
from app.db_handler.matchup import PaginatedMatchups
from app.mod_tournament.models import Matchup

bp = Blueprint("matchup", __name__, url_prefix="/matchup")


@bp.get("")
def get_matchups():
    args = request.args
    result: PaginatedMatchups = DBHandler.get_matchups(
        tournament=[*args.getlist("tournament"), *args.getlist("t")],
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
# @roles_accepted("operational", "admin")
def get_matchup_teams(matchup_id: int):
    matchup = DBHandler.get_matchup_by_id(matchup_id)
    if matchup is None:
        return {"msg": "Matchup not found"}, 404

    teams = DBHandler.get_teams_from_matchup(
        matchup.tournament_id, [matchup.team1_id, matchup.team2_id]
    )
    return {
        "id": matchup_id,
        **{
            f"team{team[0]+1}": {
                "name": [t.team.name for t in teams if t.team.id == team[1].team.id][0],
                "id": team[1].team.id,
                "players": [
                    player.to_dict(only=("id", "nickname", "role")) for player in team[1].players
                ],
            }
            for team in enumerate(teams)
        },
    }


@bp.post("")
# @roles_accepted("operational", "admin")
def post_matchup():
    data = {**request.json}
    tournament = DBHandler.get_tournament_by_id(data["tournament_id"])
    if tournament is None:
        return {"msg": "Tournament not found"}, 404

    matchup = Matchup(**data)

    if "phases" in tournament.extra:
        _phase = [phase for phase in tournament.extra["phases"] if phase["name"] == matchup.phase]
        if len(_phase) == 1:
            _phase = _phase[0]
            matchup.with_global_ban = data.get("with_global_ban", _phase["with_global_ban"])
            matchup.last_no_global_ban = data.get(
                "last_no_global_ban", _phase["last_no_global_ban"]
            )
            matchup.bo_size = data.get("bo_size", _phase["bo_size"])

    matchup = DBHandler.create_update_matchup(matchup)

    return {"id": matchup.id}, 201
