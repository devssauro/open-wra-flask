SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament_id as tournament_id,
    mm.blue_side as team_id,
    mm.winner = mm.blue_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.blue_ban_1 as ban_id,
    mm.blue_pick_1 as pick_id,
    1 as position,
    1 as pick_rotation,
    1 as ban_rotation,
    is_blind(mm.id, 'blue', 1, CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold,
    mm.blue_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.blue_side AS first_blood,
	CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_blood
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_blood
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_blood
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_blood
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_death
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_death
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_death
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_death
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.blue_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.blue_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.blue_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.blue_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.blue_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.blue_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.blue_turrets_destroyed AS torrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament_id as tournament_id,
    mm.blue_side as team_id,
    mm.winner = mm.blue_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.blue_ban_2 as ban_id,
    mm.blue_pick_2 as pick_id,
    2 as position,
    2 as pick_rotation,
    1 as ban_rotation,
    is_blind(mm.id, 'blue', 2, CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold,
    mm.blue_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.blue_side AS first_blood,
	CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_blood
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_blood
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_blood
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_blood
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_death
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_death
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_death
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_death
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.blue_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.blue_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.blue_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.blue_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.blue_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.blue_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.blue_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament_id as tournament_id,
    mm.blue_side as team_id,
    mm.winner = mm.blue_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.blue_ban_3 as ban_id,
    mm.blue_pick_3 as pick_id,
    3 as position,
    2 as pick_rotation,
    1 as ban_rotation,
    is_blind(mm.id, 'blue', 2, CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold,
    mm.blue_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.blue_side AS first_blood,
	CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_blood
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_blood
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_blood
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_blood
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_death
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_death
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_death
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_death
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.blue_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.blue_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.blue_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.blue_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.blue_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.blue_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.blue_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament_id as tournament_id,
    mm.blue_side as team_id,
    mm.winner = mm.blue_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.blue_ban_4 as ban_id,
    mm.blue_pick_4 as pick_id,
    4 as position,
    3 as pick_rotation,
    2 as ban_rotation,
    is_blind(mm.id, 'blue', 3, CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold,
    mm.blue_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.blue_side AS first_blood,
	CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_blood
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_blood
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_blood
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_blood
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_death
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_death
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_death
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_death
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.blue_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.blue_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.blue_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.blue_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.blue_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.blue_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.blue_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'blue' as side,
    mm.tournament_id as tournament_id,
    mm.blue_side as team_id,
    mm.winner = mm.blue_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.blue_ban_5 as ban_id,
    mm.blue_pick_5 as pick_id,
    5 as position,
    3 as pick_rotation,
    2 as ban_rotation,
    is_blind(mm.id, 'blue', 3, CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN 'baron'
        WHEN mm.blue_jungle_pick THEN 'jungle'
        WHEN mm.blue_mid_pick THEN 'mid'
        WHEN mm.blue_dragon_pick THEN 'dragon'
        WHEN mm.blue_sup_pick THEN 'sup'
    END role,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player
    END player,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_kills
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_kills
        WHEN mm.blue_mid_pick THEN mm.blue_mid_kills
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_kills
        WHEN mm.blue_sup_pick THEN mm.blue_sup_kills
    END kills,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_deaths
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_deaths
        WHEN mm.blue_mid_pick THEN mm.blue_mid_deaths
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_deaths
        WHEN mm.blue_sup_pick THEN mm.blue_sup_deaths
    END deaths,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_assists
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_assists
        WHEN mm.blue_mid_pick THEN mm.blue_mid_assists
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_assists
        WHEN mm.blue_sup_pick THEN mm.blue_sup_assists
    END assists,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_taken
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_taken
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_taken
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_taken
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_taken
    END dmg_taken,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_dmg_dealt
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_dmg_dealt
        WHEN mm.blue_mid_pick THEN mm.blue_mid_dmg_dealt
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_dmg_dealt
        WHEN mm.blue_sup_pick THEN mm.blue_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_total_gold
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_total_gold
        WHEN mm.blue_mid_pick THEN mm.blue_mid_total_gold
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_total_gold
        WHEN mm.blue_sup_pick THEN mm.blue_sup_total_gold
    END total_gold,
    mm.blue_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.blue_side AS first_blood,
	CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_blood
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_blood
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_blood
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_blood
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN mm.blue_baron_player = mm.player_first_death
        WHEN mm.blue_jungle_pick THEN mm.blue_jungle_player = mm.player_first_death
        WHEN mm.blue_mid_pick THEN mm.blue_mid_player = mm.player_first_death
        WHEN mm.blue_dragon_pick THEN mm.blue_dragon_player = mm.player_first_death
        WHEN mm.blue_sup_pick THEN mm.blue_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.blue_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.blue_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.blue_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.blue_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.blue_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.blue_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.blue_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament_id as tournament_id,
    mm.red_side as team_id,
    mm.winner = mm.red_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.red_ban_1 as ban_id,
    mm.red_pick_1 as pick_id,
    1 as position,
    1 as pick_rotation,
    1 as ban_rotation,
    is_blind(mm.id, 'red', 1, CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold,
    mm.red_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.red_side AS first_blood,
	CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_blood
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_blood
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_blood
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_blood
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_death
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_death
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_death
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_death
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.red_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.red_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.red_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.red_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.red_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.red_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.red_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament_id as tournament_id,
    mm.red_side as team_id,
    mm.winner = mm.red_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.red_ban_2 as ban_id,
    mm.red_pick_2 as pick_id,
    2 as position,
    1 as pick_rotation,
    1 as ban_rotation,
    is_blind(mm.id, 'red', 1, CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold,
    mm.red_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.red_side AS first_blood,
	CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_blood
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_blood
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_blood
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_blood
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_death
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_death
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_death
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_death
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.red_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.red_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.red_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.red_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.red_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.red_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.red_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament_id as tournament_id,
    mm.red_side as team_id,
    mm.winner = mm.red_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.red_ban_3 as ban_id,
    mm.red_pick_3 as pick_id,
    3 as position,
    2 as pick_rotation,
    1 as ban_rotation,
    is_blind(mm.id, 'red', 2, CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold,
    mm.red_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.red_side AS first_blood,
	CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_blood
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_blood
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_blood
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_blood
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_death
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_death
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_death
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_death
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.red_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.red_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.red_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.red_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.red_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.red_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.red_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament_id as tournament_id,
    mm.red_side as team_id,
    mm.winner = mm.red_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.red_ban_4 as ban_id,
    mm.red_pick_4 as pick_id,
    4 as position,
    3 as pick_rotation,
    2 as ban_rotation,
    is_blind(mm.id, 'red', 3, CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold,
    mm.red_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.red_side AS first_blood,
	CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_blood
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_blood
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_blood
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_blood
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_death
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_death
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_death
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_death
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.red_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.red_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.red_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.red_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.red_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.red_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.red_turrets_destroyed
FROM matchup_map as mm
UNION ALL
SELECT
    uuid_generate_v4() as uuid,
    mm.matchup_id as matchup_id,
    mm.id as map_id,
    mm.map_number as map_number,
    mm.patch as patch,
    'red' as side,
    mm.tournament_id as tournament_id,
    mm.red_side as team_id,
    mm.winner = mm.red_side as winner,
    mm.length as length,
    to_seconds(mm.length) as length_sec,
    mm.red_ban_5 as ban_id,
    mm.red_pick_5 as pick_id,
    5 as position,
    4 as pick_rotation,
    2 as ban_rotation,
    is_blind(mm.id, 'red', 3, CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END) as is_blind,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN 'baron'
        WHEN mm.red_jungle_pick THEN 'jungle'
        WHEN mm.red_mid_pick THEN 'mid'
        WHEN mm.red_dragon_pick THEN 'dragon'
        WHEN mm.red_sup_pick THEN 'sup'
    END role,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_player
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player
        WHEN mm.red_mid_pick THEN mm.red_mid_player
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player
        WHEN mm.red_sup_pick THEN mm.red_sup_player
    END player,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_kills
        WHEN mm.red_jungle_pick THEN mm.red_jungle_kills
        WHEN mm.red_mid_pick THEN mm.red_mid_kills
        WHEN mm.red_dragon_pick THEN mm.red_dragon_kills
        WHEN mm.red_sup_pick THEN mm.red_sup_kills
    END kills,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_deaths
        WHEN mm.red_jungle_pick THEN mm.red_jungle_deaths
        WHEN mm.red_mid_pick THEN mm.red_mid_deaths
        WHEN mm.red_dragon_pick THEN mm.red_dragon_deaths
        WHEN mm.red_sup_pick THEN mm.red_sup_deaths
    END deaths,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_assists
        WHEN mm.red_jungle_pick THEN mm.red_jungle_assists
        WHEN mm.red_mid_pick THEN mm.red_mid_assists
        WHEN mm.red_dragon_pick THEN mm.red_dragon_assists
        WHEN mm.red_sup_pick THEN mm.red_sup_assists
    END assists,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_taken
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_taken
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_taken
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_taken
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_taken
    END dmg_taken,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_dmg_dealt
        WHEN mm.red_jungle_pick THEN mm.red_jungle_dmg_dealt
        WHEN mm.red_mid_pick THEN mm.red_mid_dmg_dealt
        WHEN mm.red_dragon_pick THEN mm.red_dragon_dmg_dealt
        WHEN mm.red_sup_pick THEN mm.red_sup_dmg_dealt
    END dmg_dealt,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_total_gold
        WHEN mm.red_jungle_pick THEN mm.red_jungle_total_gold
        WHEN mm.red_mid_pick THEN mm.red_mid_total_gold
        WHEN mm.red_dragon_pick THEN mm.red_dragon_total_gold
        WHEN mm.red_sup_pick THEN mm.red_sup_total_gold
    END total_gold,
    mm.red_turrets_destroyed as turrets_destroyed,
	mm.team_first_blood = mm.red_side AS first_blood,
	CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_blood
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_blood
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_blood
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_blood
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_blood
    END is_player_first_blood,
	CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN mm.red_baron_player = mm.player_first_death
        WHEN mm.red_jungle_pick THEN mm.red_jungle_player = mm.player_first_death
        WHEN mm.red_mid_pick THEN mm.red_mid_player = mm.player_first_death
        WHEN mm.red_dragon_pick THEN mm.red_dragon_player = mm.player_first_death
        WHEN mm.red_sup_pick THEN mm.red_sup_player = mm.player_first_death
    END is_player_first_death,
	mm.place_first_blood,
	mm.team_first_herald = mm.red_side AS first_herald,
	mm.first_herald_teamfight,
	mm.first_herald_stealed,
	mm.first_herald_route,
	mm.team_second_herald = mm.red_side AS second_herald,
	mm.second_herald_teamfight,
	mm.second_herald_stealed,
	mm.second_herald_route,
	mm.team_first_tower = mm.red_side AS first_tower,
	mm.first_tower_route,
	mm.first_tower_herald,
	mm.team_first_drake = mm.red_side AS first_drake,
	mm.first_drake_teamfight,
    mm.first_drake_stealed,
    mm.first_drake_type,
	mm.team_second_drake = mm.red_side AS second_drake,
	mm.second_drake_teamfight,
	mm.second_drake_stealed,
	mm.second_drake_type,
	mm.team_third_drake = mm.red_side AS third_drake,
	mm.third_drake_teamfight,
	mm.third_drake_stealed,
	mm.third_drake_type,
	mm.red_turrets_destroyed
FROM matchup_map as mm
