from flask import Request
from flask_login import current_user
from sqlalchemy import Integer, String, and_, case, cast, func
from sqlalchemy.orm import aliased

from app.mod_team.models import Player, Team
from app.mod_tournament.models import Champion, Matchup, MatchupMap, Tournament
from app.mod_view.models import ObjectiveView, PicksBansPrioView, SingleView

ROLES = ["baron", "jungle", "mid", "dragon", "sup"]


def binary_types(column, return_type, iso_return_type, label: str = None):
    if iso_return_type is not None:
        return_type = iso_return_type
    if label is None and iso_return_type is not None:
        label = iso_return_type
    if return_type == "numeric":
        return case((column.is_(None), None), else_=cast(column, Integer)).label(label)
    return case((column.is_(None), ""), (column, "true"), else_="false").label(label)


def set_file_name(
    request: Request,
    ignore: str,
    tournament: str,
    patch: str,
    team: str,
) -> str:
    file_name: str = ""
    if ignore != "t" and "t" in request.args:
        file_name = f'_{tournament.replace(" ", "_")}'
    if ignore != "patch" and "patch" in request.args:
        file_name = f'_patch_{patch.replace(".", "")}'
    if ignore != "team" and "team" in request.args:
        file_name = f'_team_{team.replace(".", "")}'
    return file_name


def get_picks_bans_view_fields(request: Request):
    pick = aliased(Champion)
    ban = aliased(Champion)

    pick_rotation = {
        "explicit_eng": case(
            (and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 1), "B1"),
            (
                and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 2),
                "B2/B3",
            ),
            (
                and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 3),
                "B4/B5",
            ),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 1), "R1/R2"),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 2), "R3"),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 3), "R4"),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 4), "R5"),
        ),
        "explicit_pt": case(
            (and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 1), "A1"),
            (
                and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 2),
                "A2/A3",
            ),
            (
                and_(PicksBansPrioView.side == "blue", PicksBansPrioView.pick_rotation == 3),
                "A4/A5",
            ),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 1), "V1/V2"),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 2), "V3"),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 3), "V4"),
            (and_(PicksBansPrioView.side == "red", PicksBansPrioView.pick_rotation == 4), "V5"),
        ),
    }
    winner_loser = {
        "explicit_eng": case((PicksBansPrioView.winner, "winner"), else_="loser").label(
            "winner_loser"
        ),
        "explicit_pt": case((PicksBansPrioView.winner, "vitória"), else_="derrota").label(
            "vencedor_perdedor"
        ),
        "letter_eng": case((PicksBansPrioView.winner, "W"), else_="L").label("W_L"),
        "letter_pt": case((PicksBansPrioView.winner, "V"), else_="D").label("V_D"),
        "numeric": cast(PicksBansPrioView.winner, Integer).label("winner"),
    }
    blind_response = {
        "explicit": case((PicksBansPrioView.is_blind, "blind"), else_="response").label(
            "blind_response"
        ),
        "letter_eng": case((PicksBansPrioView.is_blind, "B"), else_="R").label("B_R"),
        "numeric": cast(PicksBansPrioView.is_blind, Integer).label("is_blind"),
    }

    columns = [
        Tournament.name.label("tournament"),
        PicksBansPrioView.matchup_id,
        PicksBansPrioView.map_id,
        PicksBansPrioView.map_number,
        PicksBansPrioView.patch,
        Matchup.phase,
        Team.name.label("team_name"),
        Team.tag.label("team_tag"),
        winner_loser.get(
            request.args.get("winner_loser"),
            case((PicksBansPrioView.winner, "true"), else_="false").label("winner"),
        ),
        PicksBansPrioView.length,
        PicksBansPrioView.length_sec,
        PicksBansPrioView.side,
        PicksBansPrioView.position,
        PicksBansPrioView.ban_rotation,
        ban.name.label("ban"),
        pick_rotation.get(
            request.args.get("pick_rotation"), PicksBansPrioView.pick_rotation
        ).label("pick_rotation"),
        pick.name.label("pick"),
        blind_response.get(
            request.args.get("blind_response"),
            case((PicksBansPrioView.is_blind, "true"), else_="false").label("is_blind"),
        ),
        PicksBansPrioView.role,
        Player.nickname.label("player"),
        PicksBansPrioView.kills,
        PicksBansPrioView.deaths,
        PicksBansPrioView.assists,
        PicksBansPrioView.dmg_dealt,
        PicksBansPrioView.dmg_taken,
        PicksBansPrioView.total_gold,
    ]
    if current_user is not None and current_user.has_role("analyst"):
        columns = [
            *columns,
            PicksBansPrioView.turrets_destroyed,
            binary_types(
                PicksBansPrioView.first_blood,
                request.args.get("objective_type"),
                request.args.get("first_blood"),
                "first_blood",
            ),
            binary_types(
                PicksBansPrioView.is_player_first_blood,
                request.args.get("objective_type"),
                request.args.get("is_player_first_blood"),
                "is_player_first_blood",
            ),
            binary_types(
                PicksBansPrioView.is_player_first_death,
                request.args.get("objective_type"),
                request.args.get("is_player_first_death"),
                "is_player_first_death",
            ),
            PicksBansPrioView.place_first_blood,
            binary_types(
                PicksBansPrioView.first_herald,
                request.args.get("objective_type"),
                request.args.get("first_herald"),
                "first_herald",
            ),
            binary_types(
                PicksBansPrioView.first_herald_teamfight,
                request.args.get("objective_type"),
                request.args.get("first_herald_teamfight"),
                "first_herald_teamfight",
            ),
            binary_types(
                PicksBansPrioView.first_herald_stealed,
                request.args.get("objective_type"),
                request.args.get("first_herald_stealed"),
                "first_herald_stealed",
            ),
            PicksBansPrioView.first_herald_route,
            binary_types(
                PicksBansPrioView.second_herald,
                request.args.get("objective_type"),
                request.args.get("second_herald"),
                "second_herald",
            ),
            binary_types(
                PicksBansPrioView.second_herald_teamfight,
                request.args.get("objective_type"),
                request.args.get("second_herald_teamfight"),
                "second_herald_teamfight",
            ),
            binary_types(
                PicksBansPrioView.second_herald_stealed,
                request.args.get("objective_type"),
                request.args.get("second_herald_stealed"),
                "second_herald_stealed",
            ),
            PicksBansPrioView.second_herald_route,
            binary_types(
                PicksBansPrioView.first_tower,
                request.args.get("objective_type"),
                request.args.get("first_tower"),
                "first_tower",
            ),
            PicksBansPrioView.first_tower_route,
            binary_types(
                PicksBansPrioView.first_tower_herald,
                request.args.get("objective_type"),
                request.args.get("first_tower_herald"),
                "first_tower_herald",
            ),
            binary_types(
                PicksBansPrioView.first_drake,
                request.args.get("objective_type"),
                request.args.get("first_drake"),
                "first_drake",
            ),
            binary_types(
                PicksBansPrioView.first_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("first_drake_teamfight"),
                "first_drake_teamfight",
            ),
            binary_types(
                PicksBansPrioView.first_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("first_drake_stealed"),
                "first_drake_stealed",
            ),
            PicksBansPrioView.first_drake_type,
            binary_types(
                PicksBansPrioView.second_drake,
                request.args.get("objective_type"),
                request.args.get("second_drake"),
                "second_drake",
            ),
            binary_types(
                PicksBansPrioView.second_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("second_drake_teamfight"),
                "second_drake_teamfight",
            ),
            binary_types(
                PicksBansPrioView.second_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("second_drake_stealed"),
                "second_drake_stealed",
            ),
            PicksBansPrioView.second_drake_type,
            binary_types(
                PicksBansPrioView.third_drake,
                request.args.get("objective_type"),
                request.args.get("third_drake"),
                "third_drake",
            ),
            binary_types(
                PicksBansPrioView.third_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("third_drake_teamfight"),
                "third_drake_teamfight",
            ),
            binary_types(
                PicksBansPrioView.third_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("third_drake_stealed"),
                "third_drake_stealed",
            ),
            PicksBansPrioView.third_drake_type,
        ]
    joins = [
        (Tournament, Tournament.id == PicksBansPrioView.tournament_id),
        (ban, ban.id == PicksBansPrioView.ban_id),
        (pick, pick.id == PicksBansPrioView.pick_id),
        (Player, Player.id == PicksBansPrioView.player),
        (Team, Team.id == PicksBansPrioView.team_id),
        (Matchup, Matchup.id == PicksBansPrioView.matchup_id),
    ]
    return dict(columns=columns, joins=joins)


def get_single_view_fields(request: Request):
    winner_loser = {
        "explicit_eng": case(
            (SingleView.winner == SingleView.team_id, "winner"), else_="loser"
        ).label("winner_loser"),
        "explicit_pt": case(
            (SingleView.winner == SingleView.team_id, "vencedor"), else_="perdedor"
        ).label("vencedor_perdedor"),
        "letter_eng": case((SingleView.winner == SingleView.team_id, "W"), else_="L").label("W_L"),
        "letter_pt": case((SingleView.winner == SingleView.team_id, "V"), else_="D").label("V_D"),
        "numeric": cast(SingleView.winner == SingleView.team_id, Integer).label("winner"),
    }
    pick_ids = {
        "pick_1": SingleView.pick_1,
        "pick_2": SingleView.pick_2,
        "pick_3": SingleView.pick_3,
        "pick_4": SingleView.pick_4,
        "pick_5": SingleView.pick_5,
    }
    role_ids = {
        "baron_pick": SingleView.baron_pick,
        "jungle_pick": SingleView.jungle_pick,
        "mid_pick": SingleView.mid_pick,
        "dragon_pick": SingleView.dragon_pick,
        "sup_pick": SingleView.sup_pick,
    }
    role_players_ids = {
        "baron_player": SingleView.baron_player,
        "jungle_player": SingleView.jungle_player,
        "mid_player": SingleView.mid_player,
        "dragon_player": SingleView.dragon_player,
        "sup_player": SingleView.sup_player,
    }
    ban_ids = {
        "ban_1": SingleView.ban_1,
        "ban_2": SingleView.ban_2,
        "ban_3": SingleView.ban_3,
        "ban_4": SingleView.ban_4,
        "ban_5": SingleView.ban_5,
    }
    bans = {f"ban_{n + 1}": aliased(Champion) for n in range(5)}
    picks = {f"pick_{n + 1}": aliased(Champion) for n in range(5)}
    role_pick = {f"{r}_pick": aliased(Champion) for r in ROLES}
    role_player = {f"{r}_player": aliased(Player) for r in ROLES}
    role_fields = [
        SingleView.baron_kills,
        SingleView.baron_deaths,
        SingleView.baron_assists,
        SingleView.baron_dmg_taken,
        SingleView.baron_dmg_dealt,
        SingleView.baron_total_gold,
        SingleView.jungle_kills,
        SingleView.jungle_deaths,
        SingleView.jungle_assists,
        SingleView.jungle_dmg_taken,
        SingleView.jungle_dmg_dealt,
        SingleView.jungle_total_gold,
        SingleView.mid_kills,
        SingleView.mid_deaths,
        SingleView.mid_assists,
        SingleView.mid_dmg_taken,
        SingleView.mid_dmg_dealt,
        SingleView.mid_total_gold,
        SingleView.dragon_kills,
        SingleView.dragon_deaths,
        SingleView.dragon_assists,
        SingleView.dragon_dmg_taken,
        SingleView.dragon_dmg_dealt,
        SingleView.dragon_total_gold,
        SingleView.sup_kills,
        SingleView.sup_deaths,
        SingleView.sup_assists,
        SingleView.sup_dmg_taken,
        SingleView.sup_dmg_dealt,
        SingleView.sup_total_gold,
    ]
    joins = [
        (Tournament, Tournament.id == SingleView.tournament_id),
        (Team, Team.id == SingleView.team_id),
        (Matchup, Matchup.id == SingleView.matchup_id),
        *[(bans[p], ban_ids[p] == bans[p].id) for p in ban_ids.keys()],
        *[(picks[p], pick_ids[p] == picks[p].id) for p in pick_ids.keys()],
        *[(role_pick[r], role_ids[r] == role_pick[r].id) for r in role_pick.keys()],
        *[(role_player[r], role_players_ids[r] == role_player[r].id) for r in role_player.keys()],
    ]

    columns = [
        Tournament.name.label("tournament"),
        Team.name.label("team_name"),
        Team.tag.label("team_tag"),
        Matchup.phase,
        SingleView.patch,
        SingleView.matchup_id,
        SingleView.map_id,
        SingleView.map_number,
        SingleView.side,
        SingleView.length,
        SingleView.length_sec,
        winner_loser.get(
            request.args.get("winner_loser"),
            case((SingleView.winner == SingleView.team_id, "true"), else_="false").label("winner"),
        ),
        SingleView.winner_side,
        *[bans[r].name.label(r) for r in bans.keys()],
        *[picks[r].name.label(r) for r in picks.keys()],
        *[role_pick[r].name.label(r) for r in role_pick.keys()],
        *[role_player[r].nickname.label(r) for r in role_player.keys()],
        *role_fields,
    ]
    if current_user is not None and current_user.has_role("analyst"):
        first_death_player = aliased(Player)
        first_blood_player = aliased(Player)
        joins = [
            *joins,
            (first_blood_player, first_blood_player.id == SingleView.player_first_blood),
            (first_death_player, first_death_player.id == SingleView.player_first_death),
        ]
        columns = [
            *columns,
            SingleView.turrets_destroyed,
            first_blood_player.nickname.label("first_blood_player"),
            first_death_player.nickname.label("first_death_player"),
            binary_types(
                SingleView.first_blood,
                request.args.get("objective_type"),
                request.args.get("first_blood"),
                "first_blood",
            ),
            SingleView.place_first_blood,
            binary_types(
                SingleView.first_herald,
                request.args.get("objective_type"),
                request.args.get("first_herald"),
                "first_herald",
            ),
            binary_types(
                SingleView.first_herald_teamfight,
                request.args.get("objective_type"),
                request.args.get("first_herald_teamfight"),
                "first_herald_teamfight",
            ),
            binary_types(
                SingleView.first_herald_stealed,
                request.args.get("objective_type"),
                request.args.get("first_herald_stealed"),
                "first_herald_stealed",
            ),
            SingleView.first_herald_route,
            binary_types(
                SingleView.second_herald,
                request.args.get("objective_type"),
                request.args.get("second_herald"),
                "second_herald",
            ),
            binary_types(
                SingleView.second_herald_teamfight,
                request.args.get("objective_type"),
                request.args.get("second_herald_teamfight"),
                "second_herald_teamfight",
            ),
            binary_types(
                SingleView.second_herald_stealed,
                request.args.get("objective_type"),
                request.args.get("second_herald_stealed"),
                "second_herald_stealed",
            ),
            SingleView.second_herald_route,
            binary_types(
                SingleView.first_tower,
                request.args.get("objective_type"),
                request.args.get("first_tower"),
                "first_tower",
            ),
            SingleView.first_tower_route,
            binary_types(
                SingleView.first_tower_herald,
                request.args.get("objective_type"),
                request.args.get("first_tower_herald"),
                "first_tower_herald",
            ),
            binary_types(
                SingleView.first_drake,
                request.args.get("objective_type"),
                request.args.get("first_drake"),
                "first_drake",
            ),
            binary_types(
                SingleView.first_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("first_drake_teamfight"),
                "first_drake_teamfight",
            ),
            binary_types(
                SingleView.first_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("first_drake_stealed"),
                "first_drake_stealed",
            ),
            SingleView.first_drake_type,
            binary_types(
                SingleView.second_drake,
                request.args.get("objective_type"),
                request.args.get("second_drake"),
                "second_drake",
            ),
            binary_types(
                SingleView.second_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("second_drake_teamfight"),
                "second_drake_teamfight",
            ),
            binary_types(
                SingleView.second_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("second_drake_stealed"),
                "second_drake_stealed",
            ),
            SingleView.second_drake_type,
            binary_types(
                SingleView.third_drake,
                request.args.get("objective_type"),
                request.args.get("third_drake"),
                "third_drake",
            ),
            binary_types(
                SingleView.third_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("third_drake_teamfight"),
                "third_drake_teamfight",
            ),
            binary_types(
                SingleView.third_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("third_drake_stealed"),
                "third_drake_stealed",
            ),
            SingleView.third_drake_type,
        ]

    return dict(columns=columns, joins=joins)


def get_full_map_fields(request: Request):
    team1 = aliased(Team)
    team2 = aliased(Team)
    pick_ids = {
        "blue_pick_1": MatchupMap.blue_pick_1,
        "blue_pick_2": MatchupMap.blue_pick_2,
        "blue_pick_3": MatchupMap.blue_pick_3,
        "blue_pick_4": MatchupMap.blue_pick_4,
        "blue_pick_5": MatchupMap.blue_pick_5,
        "red_pick_1": MatchupMap.red_pick_1,
        "red_pick_2": MatchupMap.red_pick_2,
        "red_pick_3": MatchupMap.red_pick_3,
        "red_pick_4": MatchupMap.red_pick_4,
        "red_pick_5": MatchupMap.red_pick_5,
    }
    role_ids = {
        "blue_baron_pick": MatchupMap.blue_baron_pick,
        "blue_jungle_pick": MatchupMap.blue_jungle_pick,
        "blue_mid_pick": MatchupMap.blue_mid_pick,
        "blue_dragon_pick": MatchupMap.blue_dragon_pick,
        "blue_sup_pick": MatchupMap.blue_sup_pick,
        "red_baron_pick": MatchupMap.red_baron_pick,
        "red_jungle_pick": MatchupMap.red_jungle_pick,
        "red_mid_pick": MatchupMap.red_mid_pick,
        "red_dragon_pick": MatchupMap.red_dragon_pick,
        "red_sup_pick": MatchupMap.red_sup_pick,
    }
    role_players_ids = {
        "blue_baron_player": MatchupMap.blue_baron_player,
        "blue_jungle_player": MatchupMap.blue_jungle_player,
        "blue_mid_player": MatchupMap.blue_mid_player,
        "blue_dragon_player": MatchupMap.blue_dragon_player,
        "blue_sup_player": MatchupMap.blue_sup_player,
        "red_baron_player": MatchupMap.red_baron_player,
        "red_jungle_player": MatchupMap.red_jungle_player,
        "red_mid_player": MatchupMap.red_mid_player,
        "red_dragon_player": MatchupMap.red_dragon_player,
        "red_sup_player": MatchupMap.red_sup_player,
    }
    ban_ids = {
        "blue_ban_1": MatchupMap.blue_ban_1,
        "blue_ban_2": MatchupMap.blue_ban_2,
        "blue_ban_3": MatchupMap.blue_ban_3,
        "blue_ban_4": MatchupMap.blue_ban_4,
        "blue_ban_5": MatchupMap.blue_ban_5,
        "red_ban_1": MatchupMap.red_ban_1,
        "red_ban_2": MatchupMap.red_ban_2,
        "red_ban_3": MatchupMap.red_ban_3,
        "red_ban_4": MatchupMap.red_ban_4,
        "red_ban_5": MatchupMap.red_ban_5,
    }
    bans = {f"{side}_ban_{n + 1}": aliased(Champion) for n in range(5) for side in ("blue", "red")}
    picks = {
        f"{side}_pick_{n + 1}": aliased(Champion) for n in range(5) for side in ("blue", "red")
    }
    role_pick = {f"{side}_{r}_pick": aliased(Champion) for r in ROLES for side in ("blue", "red")}
    role_player = {
        f"{side}_{r}_player": aliased(Player) for r in ROLES for side in ("blue", "red")
    }
    role_fields = [
        MatchupMap.blue_baron_kills,
        MatchupMap.blue_baron_deaths,
        MatchupMap.blue_baron_assists,
        MatchupMap.blue_baron_dmg_taken,
        MatchupMap.blue_baron_dmg_dealt,
        MatchupMap.blue_baron_total_gold,
        MatchupMap.blue_jungle_kills,
        MatchupMap.blue_jungle_deaths,
        MatchupMap.blue_jungle_assists,
        MatchupMap.blue_jungle_dmg_taken,
        MatchupMap.blue_jungle_dmg_dealt,
        MatchupMap.blue_jungle_total_gold,
        MatchupMap.blue_mid_kills,
        MatchupMap.blue_mid_deaths,
        MatchupMap.blue_mid_assists,
        MatchupMap.blue_mid_dmg_taken,
        MatchupMap.blue_mid_dmg_dealt,
        MatchupMap.blue_mid_total_gold,
        MatchupMap.blue_dragon_kills,
        MatchupMap.blue_dragon_deaths,
        MatchupMap.blue_dragon_assists,
        MatchupMap.blue_dragon_dmg_taken,
        MatchupMap.blue_dragon_dmg_dealt,
        MatchupMap.blue_dragon_total_gold,
        MatchupMap.blue_sup_kills,
        MatchupMap.blue_sup_deaths,
        MatchupMap.blue_sup_assists,
        MatchupMap.blue_sup_dmg_taken,
        MatchupMap.blue_sup_dmg_dealt,
        MatchupMap.blue_sup_total_gold,
        MatchupMap.red_baron_kills,
        MatchupMap.red_baron_deaths,
        MatchupMap.red_baron_assists,
        MatchupMap.red_baron_dmg_taken,
        MatchupMap.red_baron_dmg_dealt,
        MatchupMap.red_baron_total_gold,
        MatchupMap.red_jungle_kills,
        MatchupMap.red_jungle_deaths,
        MatchupMap.red_jungle_assists,
        MatchupMap.red_jungle_dmg_taken,
        MatchupMap.red_jungle_dmg_dealt,
        MatchupMap.red_jungle_total_gold,
        MatchupMap.red_mid_kills,
        MatchupMap.red_mid_deaths,
        MatchupMap.red_mid_assists,
        MatchupMap.red_mid_dmg_taken,
        MatchupMap.red_mid_dmg_dealt,
        MatchupMap.red_mid_total_gold,
        MatchupMap.red_dragon_kills,
        MatchupMap.red_dragon_deaths,
        MatchupMap.red_dragon_assists,
        MatchupMap.red_dragon_dmg_taken,
        MatchupMap.red_dragon_dmg_dealt,
        MatchupMap.red_dragon_total_gold,
        MatchupMap.red_sup_kills,
        MatchupMap.red_sup_deaths,
        MatchupMap.red_sup_assists,
        MatchupMap.red_sup_dmg_taken,
        MatchupMap.red_sup_dmg_dealt,
        MatchupMap.red_sup_total_gold,
    ]
    joins = [
        (Tournament, Tournament.id == MatchupMap.tournament_id),
        (team1, team1.id == MatchupMap.blue_side),
        (team2, team2.id == MatchupMap.red_side),
        (Matchup, Matchup.id == MatchupMap.matchup_id),
        *[(bans[p], ban_ids[p] == bans[p].id) for p in ban_ids.keys()],
        *[(picks[p], pick_ids[p] == picks[p].id) for p in pick_ids.keys()],
        *[(role_pick[r], role_ids[r] == role_pick[r].id) for r in role_pick.keys()],
        *[(role_player[r], role_players_ids[r] == role_player[r].id) for r in role_player.keys()],
    ]

    columns = [
        Tournament.name.label("tournament"),
        team1.name.label("blue_side_team"),
        team1.tag.label("blue_side_tag"),
        team2.name.label("red_side_team"),
        team2.tag.label("red_side_tag"),
        Matchup.phase,
        MatchupMap.patch,
        MatchupMap.matchup_id,
        MatchupMap.id,
        MatchupMap.map_number,
        MatchupMap.length,
        func.to_seconds(MatchupMap.length).label("length_sec"),
        case((MatchupMap.winner == team1.id, team1.tag), else_=team2.tag).label("winner"),
        MatchupMap.winner_side,
        *[bans[r].name.label(r) for r in bans.keys()],
        *[picks[r].name.label(r) for r in picks.keys()],
        *[role_pick[r].name.label(r) for r in role_pick.keys()],
        *[role_player[r].nickname.label(r) for r in role_player.keys()],
        *role_fields,
    ]
    if current_user is not None and current_user.has_role("analyst"):
        first_death_player = aliased(Player)
        first_blood_player = aliased(Player)
        objectives_ids = {
            "team_first_blood": MatchupMap.team_first_blood,
            "team_first_tower": MatchupMap.team_first_tower,
            "team_first_herald": MatchupMap.team_first_herald,
            "team_second_herald": MatchupMap.team_second_herald,
            "team_first_drake": MatchupMap.team_first_drake,
            "team_second_drake": MatchupMap.team_second_drake,
            "team_third_drake": MatchupMap.team_third_drake,
        }
        objectives = {
            objective: aliased(Team)
            for objective in (
                "team_first_blood",
                "team_first_tower",
                "team_first_herald",
                "team_second_herald",
                "team_first_drake",
                "team_second_drake",
                "team_third_drake",
            )
        }
        joins = [
            *joins,
            (first_blood_player, first_blood_player.id == MatchupMap.player_first_blood),
            (first_death_player, first_death_player.id == MatchupMap.player_first_death),
            *[
                (objectives[o], objectives[o].id == objectives_ids[o])
                for o in objectives_ids.keys()
            ],
        ]
        columns = [
            *columns,
            MatchupMap.blue_turrets_destroyed,
            MatchupMap.red_turrets_destroyed,
            objectives["team_first_blood"].name.label("team_first_blood_name"),
            objectives["team_first_blood"].tag.label("team_first_blood_tag"),
            first_blood_player.nickname.label("first_blood_player"),
            first_death_player.nickname.label("first_death_player"),
            MatchupMap.place_first_blood,
            objectives["team_first_herald"].name.label("team_first_herald_name"),
            objectives["team_first_herald"].tag.label("team_first_herald_tag"),
            binary_types(
                MatchupMap.first_herald_teamfight,
                request.args.get("objective_type"),
                request.args.get("first_herald_teamfight"),
                "first_herald_teamfight",
            ),
            binary_types(
                MatchupMap.first_herald_stealed,
                request.args.get("objective_type"),
                request.args.get("first_herald_stealed"),
                "first_herald_stealed",
            ),
            MatchupMap.first_herald_route,
            objectives["team_second_herald"].name.label("team_second_herald_name"),
            objectives["team_second_herald"].tag.label("team_second_herald_tag"),
            binary_types(
                MatchupMap.second_herald_teamfight,
                request.args.get("objective_type"),
                request.args.get("second_herald_teamfight"),
                "second_herald_teamfight",
            ),
            binary_types(
                MatchupMap.second_herald_stealed,
                request.args.get("objective_type"),
                request.args.get("second_herald_stealed"),
                "second_herald_stealed",
            ),
            MatchupMap.second_herald_route,
            objectives["team_first_tower"].name.label("team_first_tower_name"),
            objectives["team_first_tower"].tag.label("team_first_tower_tag"),
            cast(MatchupMap.first_tower_route, String).label("first_tower_route"),
            binary_types(
                MatchupMap.first_tower_herald,
                request.args.get("objective_type"),
                request.args.get("first_tower_herald"),
                "first_tower_herald",
            ),
            objectives["team_first_drake"].name.label("team_first_drake_name"),
            objectives["team_first_drake"].tag.label("team_first_drake_tag"),
            binary_types(
                MatchupMap.first_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("first_drake_teamfight"),
                "first_drake_teamfight",
            ),
            binary_types(
                MatchupMap.first_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("first_drake_stealed"),
                "first_drake_stealed",
            ),
            MatchupMap.first_drake_type,
            objectives["team_second_drake"].name.label("team_second_drake_name"),
            objectives["team_second_drake"].tag.label("team_second_drake_tag"),
            binary_types(
                MatchupMap.second_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("second_drake_teamfight"),
                "second_drake_teamfight",
            ),
            binary_types(
                MatchupMap.second_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("second_drake_stealed"),
                "second_drake_stealed",
            ),
            MatchupMap.second_drake_type,
            objectives["team_third_drake"].name.label("team_third_drake_name"),
            objectives["team_third_drake"].tag.label("team_third_drake_tag"),
            binary_types(
                MatchupMap.third_drake_teamfight,
                request.args.get("objective_type"),
                request.args.get("third_drake_teamfight"),
                "third_drake_teamfight",
            ),
            binary_types(
                MatchupMap.third_drake_stealed,
                request.args.get("objective_type"),
                request.args.get("third_drake_stealed"),
                "third_drake_stealed",
            ),
            MatchupMap.third_drake_type,
        ]

    return dict(columns=columns, joins=joins)


def get_objective_fields(request: Request):
    team_taker = aliased(Team)
    killer, victim = aliased(Player), aliased(Player)
    champion_killer, champion_victim = aliased(Champion), aliased(Champion)
    winner_loser = {
        "explicit_eng": case((ObjectiveView.winner, "winner"), else_="loser").label(
            "winner_loser"
        ),
        "explicit_pt": case((ObjectiveView.winner, "vitória"), else_="derrota").label(
            "vencedor_perdedor"
        ),
        "letter_eng": case((ObjectiveView.winner, "W"), else_="L").label("W_L"),
        "letter_pt": case((ObjectiveView.winner, "V"), else_="D").label("V_D"),
        "numeric": cast(ObjectiveView.winner, Integer).label("winner"),
    }
    joins = [
        (Tournament, Tournament.id == ObjectiveView.tournament_id),
        (Matchup, Matchup.id == ObjectiveView.matchup_id),
        (MatchupMap, MatchupMap.id == ObjectiveView.map_id),
        (team_taker, team_taker.id == ObjectiveView.team_id),
        (killer, killer.id == ObjectiveView.killer),
        (victim, victim.id == ObjectiveView.victim),
        (champion_killer, champion_killer.id == ObjectiveView.champion_killer),
        (champion_victim, champion_victim.id == ObjectiveView.champion_victim),
    ]

    columns = [
        Tournament.name.label("tournament"),
        team_taker.name.label("team_name"),
        team_taker.tag.label("team_tag"),
        Matchup.phase,
        ObjectiveView.patch,
        ObjectiveView.matchup_id,
        ObjectiveView.map_id.label("map_id"),
        ObjectiveView.map_number,
        ObjectiveView.side,
        ObjectiveView.length,
        ObjectiveView.length_sec,
        winner_loser.get(
            request.args.get("winner_loser"),
            case((ObjectiveView.winner, "true"), else_="false").label("winner"),
        ),
        ObjectiveView.objective_type,
        ObjectiveView.objective_name,
        ObjectiveView.objective_order,
        binary_types(
            ObjectiveView.with_teamfight,
            request.args.get("objective_details"),
            request.args.get("with_teamfight"),
            "with_teamfight",
        ),
        binary_types(
            ObjectiveView.is_stealed,
            request.args.get("objective_details"),
            request.args.get("is_stealed"),
            "is_stealed",
        ),
        ObjectiveView.place,
        binary_types(
            ObjectiveView.with_herald,
            request.args.get("objective_details"),
            request.args.get("with_herald"),
            "with_herald",
        ),
        killer.nickname.label("killer"),
        ObjectiveView.role_killer,
        champion_killer.name.label("champion_killer"),
        victim.nickname.label("victim"),
        ObjectiveView.role_victim,
        champion_victim.name.label("champion_victim"),
    ]

    return dict(columns=columns, joins=joins)
