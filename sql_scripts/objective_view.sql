SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_first_herald
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_first_herald AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_first_herald AS team_id,
    CASE mm.team_first_herald
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'herald' AS objective_type,
	null AS objective_name,
	1 AS objective_order,
	mm.first_herald_teamfight AS with_teamfight,
	mm.first_herald_stealed AS is_stealed,
	mm.first_herald_route AS place,
	CAST(null AS BOOLEAN) AS with_herald,
	CAST(null AS INT) AS killer,
	CAST(null AS VARCHAR) AS role_killer,
	CAST(null AS INT) AS champion_killer,
	CAST(null AS INT) AS victim,
	CAST(null AS VARCHAR) AS role_victim,
	CAST(null AS INT) AS champion_victim
FROM matchup_map AS mm
UNION ALL
SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_second_herald
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_second_herald AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_second_herald AS team_id,
    CASE mm.team_second_herald
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'herald' AS objective_type,
	null AS objective_name,
	2 AS objective_order,
	mm.second_herald_teamfight AS with_teamfight,
	mm.second_herald_stealed AS is_stealed,
	mm.second_herald_route AS place,
	CAST(null AS BOOLEAN) AS with_herald,
	CAST(null AS INT) AS killer,
	CAST(null AS VARCHAR) AS role_killer,
	CAST(null AS INT) AS champion_killer,
	CAST(null AS INT) AS victim,
	CAST(null AS VARCHAR) AS role_victim,
	CAST(null AS INT) AS champion_victim
FROM matchup_map AS mm
UNION ALL
SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_first_drake
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_first_drake AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_first_drake AS team_id,
    CASE mm.team_first_drake
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'drake' AS objective_type,
	mm.first_drake_type AS objective_name,
	1 AS objective_order,
	mm.first_drake_teamfight AS with_teamfight,
	mm.first_drake_stealed AS is_stealed,
	null AS place,
	CAST(null AS BOOLEAN) AS with_herald,
	CAST(null AS INT) AS killer,
	CAST(null AS VARCHAR) AS role_killer,
	CAST(null AS INT) AS champion_killer,
	CAST(null AS INT) AS victim,
	CAST(null AS VARCHAR) AS role_victim,
	CAST(null AS INT) AS champion_victim
FROM matchup_map AS mm
UNION ALL
SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_second_drake
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_second_drake AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_second_drake AS team_id,
    CASE mm.team_second_drake
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'drake' AS objective_type,
	mm.second_drake_type AS objective_name,
	2 AS objective_order,
	mm.second_drake_teamfight AS with_teamfight,
	mm.second_drake_stealed AS is_stealed,
	null AS place,
	CAST(null AS BOOLEAN) AS with_herald,
	CAST(null AS INT) AS killer,
	CAST(null AS VARCHAR) AS role_killer,
	CAST(null AS INT) AS champion_killer,
	CAST(null AS INT) AS victim,
	CAST(null AS VARCHAR) AS role_victim,
	CAST(null AS INT) AS champion_victim
FROM matchup_map AS mm
UNION ALL
SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_third_drake
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_third_drake AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_third_drake AS team_id,
    CASE mm.team_third_drake
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'drake' AS objective_type,
	mm.third_drake_type AS objective_name,
	3 AS objective_order,
	mm.third_drake_teamfight AS with_teamfight,
	mm.third_drake_stealed AS is_stealed,
	null AS place,
	CAST(null AS BOOLEAN) AS with_herald,
	CAST(null AS INT) AS killer,
	CAST(null AS VARCHAR) AS role_killer,
	CAST(null AS INT) AS champion_killer,
	CAST(null AS INT) AS victim,
	CAST(null AS VARCHAR) AS role_victim,
	CAST(null AS INT) AS champion_victim
FROM matchup_map AS mm
UNION ALL
SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_first_tower
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_first_tower AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_first_tower AS team_id,
    CASE mm.team_first_tower
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'first_tower' AS objective_type,
	CAST(mm.first_tower_route AS VARCHAR) AS objective_name,
	null AS objective_order,
	null AS with_teamfight,
	null AS is_stealed,
	CAST(mm.first_tower_route AS VARCHAR) AS place,
	mm.first_tower_herald AS with_herald,
	CAST(null AS INT) AS killer,
	CAST(null AS VARCHAR) AS role_killer,
	CAST(null AS INT) AS champion_killer,
	CAST(null AS INT) AS victim,
	CAST(null AS VARCHAR) AS role_victim,
	CAST(null AS INT) AS champion_victim
FROM matchup_map AS mm
UNION ALL
SELECT
    uuid_generate_v4() AS uuid,
    mm.matchup_id AS matchup_id,
    mm.id AS map_id,
    mm.map_number AS map_number,
    mm.patch AS patch,
    CASE mm.team_first_blood
		WHEN mm.blue_side THEN 'blue'
		WHEN mm.red_side THEN 'red'
	END AS side,
    mm.tournament_id as tournament_id,
    mm.winner = mm.team_first_blood AS winner,
    mm.length AS length,
    to_seconds(mm.length) AS length_sec,
	mm.team_first_blood AS team_id,
    CASE mm.team_first_blood
		WHEN mm.blue_side THEN mm.red_side
		WHEN mm.red_side THEN mm.blue_side
	END AS team_giver_id,
	'first_blood' AS objective_type,
	CAST(null AS VARCHAR) AS objective_name,
	null AS objective_order,
	null AS with_teamfight,
	null AS is_stealed,
	CAST(mm.place_first_blood AS VARCHAR) AS place,
	CAST(null AS BOOLEAN) AS with_herald,
	mm.player_first_blood AS player_killer,
	CASE
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_baron_player THEN 'baron'
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_jungle_player THEN 'jungle'
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_mid_player THEN 'mid'
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_dragon_player THEN 'dragon'
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_sup_player THEN 'sup'
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_baron_player THEN 'baron'
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_jungle_player THEN 'jungle'
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_mid_player THEN 'mid'
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_dragon_player THEN 'dragon'
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_sup_player THEN 'sup'
	END AS role_killer,
	CASE
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_baron_player THEN mm.blue_baron_pick
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_jungle_player THEN mm.blue_jungle_pick
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_mid_player THEN mm.blue_mid_pick
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_dragon_player THEN mm.blue_dragon_pick
		WHEN mm.team_first_blood = mm.blue_side AND mm.player_first_blood = mm.blue_sup_player THEN mm.blue_sup_pick
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_baron_player THEN mm.red_baron_pick
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_jungle_player THEN mm.red_jungle_pick
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_mid_player THEN mm.red_mid_pick
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_dragon_player THEN mm.red_dragon_pick
		WHEN mm.team_first_blood = mm.red_side AND mm.player_first_blood = mm.red_sup_player THEN mm.red_sup_pick
	END AS champion_killer,
	mm.player_first_death AS player_victim,
	CASE
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_baron_player THEN 'baron'
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_jungle_player THEN 'jungle'
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_mid_player THEN 'mid'
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_dragon_player THEN 'dragon'
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_sup_player THEN 'sup'
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_baron_player THEN 'baron'
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_jungle_player THEN 'jungle'
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_mid_player THEN 'mid'
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_dragon_player THEN 'dragon'
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_sup_player THEN 'sup'
	END AS role_victim,
	CASE
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_baron_player THEN mm.blue_baron_pick
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_jungle_player THEN mm.blue_jungle_pick
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_mid_player THEN mm.blue_mid_pick
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_dragon_player THEN mm.blue_dragon_pick
		WHEN mm.team_first_blood != mm.blue_side AND mm.player_first_death = mm.blue_sup_player THEN mm.blue_sup_pick
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_baron_player THEN mm.red_baron_pick
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_jungle_player THEN mm.red_jungle_pick
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_mid_player THEN mm.red_mid_pick
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_dragon_player THEN mm.red_dragon_pick
		WHEN mm.team_first_blood != mm.red_side AND mm.player_first_death = mm.red_sup_player THEN mm.red_sup_pick
	END AS champion_victim
FROM matchup_map AS mm
