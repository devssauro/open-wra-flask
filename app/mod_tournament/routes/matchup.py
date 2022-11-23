from typing import List

from flask import Blueprint, request
from flask_security import roles_accepted
from sqlalchemy.orm import aliased

from db_config import db

from ...mod_team.models import Team
from ..models import Matchup, MatchupMap, Tournament, TournamentTeam

bp = Blueprint("matchup", __name__, url_prefix="/matchup")


@bp.get("")
def get_matchups():
    team1 = aliased(Team, name="team1")
    team2 = aliased(Team, name="team2")

    args = []
    if "t" in request.args:
        args.append(Matchup.tournament_id.in_([int(t) for t in request.args.getlist("t")]))

    matchups = (
        Matchup.query.with_entities(
            Matchup.id,
            Matchup.phase,
            Matchup.datetime,
            Matchup.team1_id,
            team1.tag.label("team1_tag"),
            team1.name.label("team1_name"),
            Matchup.team2_id,
            team2.tag.label("team2_tag"),
            team2.name.label("team2_name"),
        )
        .outerjoin((team1, team1.id == Matchup.team1_id), (team2, team2.id == Matchup.team2_id))
        .filter(*args)
        .order_by(Matchup.datetime.desc())
    )

    maps = MatchupMap.query.filter(
        MatchupMap.tournament_id.in_([int(t) for t in request.args.getlist("t")])
    ).order_by(MatchupMap.map_number.asc())

    return {
        "matchups": [
            {
                "id": matchup.id,
                "phase": matchup.phase,
                "datetime": matchup.datetime,
                "team1": {
                    "id": matchup.team1_id,
                    "tag": matchup.team1_tag,
                    "name": matchup.team1_name,
                },
                "team2": {
                    "id": matchup.team2_id,
                    "tag": matchup.team2_tag,
                    "name": matchup.team2_name,
                },
                "maps": [
                    {
                        "id": map.id,
                        "winner": "team1" if map.winner == matchup.team1_id else "team2",
                        "winner_side": map.winner_side,
                        "length": map.length,
                        "vod_link": map.vod_link,
                    }
                    for map in [m for m in maps if m.matchup_id == matchup.id]
                ],
            }
            for matchup in matchups
        ]
    }


@bp.get("/<int:matchup_id>/teams")
def get_matchup_teams(matchup_id: int):
    matchup: List[TournamentTeam] = list(
        TournamentTeam.query.outerjoin(
            (Tournament, Tournament.id == TournamentTeam.tournament_id),
            (Matchup, Matchup.tournament_id == Tournament.id),
        ).filter(
            Matchup.id == matchup_id,
            TournamentTeam.team_id.in_([Matchup.team1_id, Matchup.team2_id]),
        )
    )
    teams = Team.query.filter(Team.id.in_([t.team_id for t in matchup]))

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
    m: Matchup = Matchup(**request.json)
    db.session.add(m)
    db.session.commit()

    return {"id": m.id}, 201
