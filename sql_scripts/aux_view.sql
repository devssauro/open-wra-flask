SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'blue'::text AS side,
    1 AS pick_rotation,
    CASE mm.blue_pick_1
        WHEN mm.blue_baron_pick THEN 'baron'::text
        WHEN mm.blue_jungle_pick THEN 'jungle'::text
        WHEN mm.blue_mid_pick THEN 'mid'::text
        WHEN mm.blue_dragon_pick THEN 'dragon'::text
        WHEN mm.blue_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'blue'::text AS side,
    2 AS pick_rotation,
    CASE mm.blue_pick_2
        WHEN mm.blue_baron_pick THEN 'baron'::text
        WHEN mm.blue_jungle_pick THEN 'jungle'::text
        WHEN mm.blue_mid_pick THEN 'mid'::text
        WHEN mm.blue_dragon_pick THEN 'dragon'::text
        WHEN mm.blue_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'blue'::text AS side,
    2 AS pick_rotation,
    CASE mm.blue_pick_3
        WHEN mm.blue_baron_pick THEN 'baron'::text
        WHEN mm.blue_jungle_pick THEN 'jungle'::text
        WHEN mm.blue_mid_pick THEN 'mid'::text
        WHEN mm.blue_dragon_pick THEN 'dragon'::text
        WHEN mm.blue_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'blue'::text AS side,
    3 AS pick_rotation,
    CASE mm.blue_pick_4
        WHEN mm.blue_baron_pick THEN 'baron'::text
        WHEN mm.blue_jungle_pick THEN 'jungle'::text
        WHEN mm.blue_mid_pick THEN 'mid'::text
        WHEN mm.blue_dragon_pick THEN 'dragon'::text
        WHEN mm.blue_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'blue'::text AS side,
    3 AS pick_rotation,
    CASE mm.blue_pick_5
        WHEN mm.blue_baron_pick THEN 'baron'::text
        WHEN mm.blue_jungle_pick THEN 'jungle'::text
        WHEN mm.blue_mid_pick THEN 'mid'::text
        WHEN mm.blue_dragon_pick THEN 'dragon'::text
        WHEN mm.blue_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'red'::text AS side,
    1 AS pick_rotation,
    CASE mm.red_pick_1
        WHEN mm.red_baron_pick THEN 'baron'::text
        WHEN mm.red_jungle_pick THEN 'jungle'::text
        WHEN mm.red_mid_pick THEN 'mid'::text
        WHEN mm.red_dragon_pick THEN 'dragon'::text
        WHEN mm.red_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'red'::text AS side,
    1 AS pick_rotation,
    CASE mm.red_pick_2
        WHEN mm.red_baron_pick THEN 'baron'::text
        WHEN mm.red_jungle_pick THEN 'jungle'::text
        WHEN mm.red_mid_pick THEN 'mid'::text
        WHEN mm.red_dragon_pick THEN 'dragon'::text
        WHEN mm.red_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'red'::text AS side,
    2 AS pick_rotation,
    CASE mm.red_pick_3
        WHEN mm.red_baron_pick THEN 'baron'::text
        WHEN mm.red_jungle_pick THEN 'jungle'::text
        WHEN mm.red_mid_pick THEN 'mid'::text
        WHEN mm.red_dragon_pick THEN 'dragon'::text
        WHEN mm.red_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'red'::text AS side,
    3 AS pick_rotation,
    CASE mm.red_pick_4
        WHEN mm.red_baron_pick THEN 'baron'::text
        WHEN mm.red_jungle_pick THEN 'jungle'::text
        WHEN mm.red_mid_pick THEN 'mid'::text
        WHEN mm.red_dragon_pick THEN 'dragon'::text
        WHEN mm.red_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
UNION ALL
SELECT uuid_generate_v4() AS uuid,
    mm.id AS map_id,
    'red'::text AS side,
    4 AS pick_rotation,
    CASE mm.red_pick_5
        WHEN mm.red_baron_pick THEN 'baron'::text
        WHEN mm.red_jungle_pick THEN 'jungle'::text
        WHEN mm.red_mid_pick THEN 'mid'::text
        WHEN mm.red_dragon_pick THEN 'dragon'::text
        WHEN mm.red_sup_pick THEN 'sup'::text
        ELSE NULL::text
    END AS role
FROM matchup_map mm
