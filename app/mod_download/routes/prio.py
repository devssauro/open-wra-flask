import csv
from io import StringIO

from flask import Blueprint, make_response, request
from flask_security import auth_required, roles_accepted

from app.mod_download.utils import (
    get_full_map_fields,
    get_objective_fields,
    get_picks_bans_view_fields,
    get_single_view_fields,
    set_file_name,
)
from app.mod_team.models import Team
from app.mod_tournament.models import MatchupMap
from app.mod_view.models import ObjectiveView, PicksBansPrioView, SingleView
from app.mod_view.utils import filter_map_data, filter_pb_data, filter_sv_data

bp = Blueprint("files", __name__, url_prefix="")


@bp.get("picks_bans")
@bp.get("picks_bans.csv")
@auth_required("token")
def get_prio_rotation():
    partial_query = get_picks_bans_view_fields(request)
    query = (
        PicksBansPrioView.query.with_entities(*partial_query["columns"])
        .outerjoin(*partial_query["joins"])
        .filter(*filter_pb_data(request))
        .order_by(
            PicksBansPrioView.matchup_id,
            PicksBansPrioView.map_id,
            PicksBansPrioView.map_number,
            PicksBansPrioView.side,
            PicksBansPrioView.position,
        )
    )
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow([c["name"] for c in query.column_descriptions])
    cw.writerows(list(query))
    output = make_response(si.getvalue())
    first_line = query[0]
    output.headers[
        "Content-Disposition"
    ] = f"""attachment; filename=picks_bans{
    set_file_name(
        request,
        tournament=first_line.tournament
            if len(request.args.getlist('t')) < 2 else '2_tournaments',
        team=first_line.team_tag if len(request.args.getlist('team')) < 2 else '2_teams',
        patch=first_line.patch if len(request.args.getlist('patch')) < 2
        else f'{request.args.getlist("patch")[0]}_to_{request.args.getlist("patch")[-1]}'
    )
    }.csv"""
    output.headers["content-disposition"] = output.headers["Content-Disposition"]
    output.headers["Content-Type"] = "text/csv"
    return output


@bp.get("match_stats")
def get_single_view():
    partial_query = get_single_view_fields(request)
    query = (
        SingleView.query.with_entities(*partial_query["columns"])
        .filter(*filter_sv_data(request))
        .outerjoin(*partial_query["joins"])
        .order_by(
            SingleView.tournament_id,
            SingleView.matchup_id,
            SingleView.map_id,
            SingleView.map_number,
            SingleView.side,
        )
    )

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow([c["name"] for c in query.column_descriptions])
    cw.writerows(list(query))
    output = make_response(si.getvalue())
    first_line = query[0]
    output.headers[
        "Content-Disposition"
    ] = f"""attachment; filename=match_stats{
        set_file_name(
            request,
            tournament=first_line.tournament
                if len(request.args.getlist('t')) < 2 else '2_tournaments',
            team=first_line.team_tag if len(request.args.getlist('team')) < 2 else '2_teams',
            patch=first_line.patch if len(request.args.getlist('patch')) < 2
            else f'{request.args.getlist("patch")[0]}_to_{request.args.getlist("patch")[-1]}'
        )
    }.csv"""
    output.headers["Content-Type"] = "text/csv"
    return output


@bp.get("map")
def get_map_view():
    partial_query = get_full_map_fields(request)
    query = (
        MatchupMap.query.with_entities(*partial_query["columns"])
        .filter(*filter_map_data(request))
        .outerjoin(*partial_query["joins"])
        .order_by(MatchupMap.tournament_id, MatchupMap.id, MatchupMap.map_number)
    )
    team_tag = ""
    if len(request.args.getlist("team")) == 1:
        team_tag = Team.query.get(int(request.args.getlist("team")[0])).tag
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow([c["name"] for c in query.column_descriptions])
    cw.writerows(list(query))
    output = make_response(si.getvalue())
    first_line = query[0]
    output.headers[
        "Content-Disposition"
    ] = f"""attachment; filename=maps{
        set_file_name(
            request,
            tournament=first_line.tournament
                if len(request.args.getlist('t')) < 2 else '2_tournaments',
            team=team_tag if len(request.args.getlist('team')) < 2 else '2_teams',
            patch=first_line.patch if len(request.args.getlist('patch')) < 2
            else f'{request.args.getlist("patch")[0]}_to_{request.args.getlist("patch")[-1]}'
        )
    }.csv"""
    output.headers["Content-Type"] = "text/csv"
    return output


@bp.get("objective")
@roles_accepted("analyst", "admin")
def get_objective_view():
    partial_query = get_objective_fields(request)
    query = (
        ObjectiveView.query.with_entities(*partial_query["columns"])
        .filter(*filter_map_data(request))
        .outerjoin(*partial_query["joins"])
        .order_by(ObjectiveView.tournament_id)
    )
    team_tag = ""
    if len(request.args.getlist("team")) == 1:
        team_tag = Team.query.get(int(request.args.getlist("team")[0])).tag
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow([c["name"] for c in query.column_descriptions])
    cw.writerows(list(query))
    output = make_response(si.getvalue())
    first_line = query[0]
    output.headers[
        "Content-Disposition"
    ] = f"""attachment; filename=objectives{
        set_file_name(
            request,
            tournament=first_line.tournament
                if len(request.args.getlist('t')) < 2 else '2_tournaments',
            team=team_tag if len(request.args.getlist('team')) < 2 else '2_teams',
            patch=first_line.patch if len(request.args.getlist('patch')) < 2
            else f'{request.args.getlist("patch")[0]}_to_{request.args.getlist("patch")[-1]}'
        )
    }.csv"""
    output.headers["Content-Type"] = "text/csv"
    return output
