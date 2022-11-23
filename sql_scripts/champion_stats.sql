SELECT
	c.name,
	ROUND(AVG(ppv.length_sec), 2) AS avg_length_sec,
	SUM(CAST(ppv.winner AS INT)) AS qty_win,
	COUNT(ppv.pick_id) qty_games,
	SUM(CASE WHEN side = 'blue' THEN 1 ELSE 0 END) qty_blue_side,
	SUM(CASE WHEN side = 'red' THEN 1 ELSE 0 END) qty_red_side,
	SUM(CASE WHEN side = 'blue' AND ppv.winner THEN 1 ELSE 0 END) win_blue_side,
	SUM(CASE WHEN side = 'red' AND ppv.winner THEN 1 ELSE 0 END) win_red_side,
	SUM(CASE WHEN ppv.is_blind THEN 1 ELSE 0 END) AS qty_blind,
	SUM(CASE WHEN ppv.is_blind AND ppv.winner THEN 1 ELSE 0 END) AS win_blind,
	SUM(CASE WHEN ppv.is_blind = false THEN 1 ELSE 0 END) AS qty_response,
	SUM(CASE WHEN ppv.is_blind = false AND ppv.winner THEN 1 ELSE 0 END) AS win_response,
	ROUND(AVG(ppv.kills), 2) AS avg_kills,
	ROUND(AVG(ppv.deaths), 2) AS avg_deaths,
	ROUND(AVG(ppv.assists), 2) AS avg_assists,
	ROUND((AVG(ppv.kills) + AVG(ppv.assists)) / AVG(ppv.deaths), 2) AS kda,
	ROUND(AVG(ppv.dmg_dealt) / (AVG(ppv.length_sec) / 60), 2) AS ddpm,
	ROUND(AVG(ppv.total_gold) / (AVG(ppv.length_sec) / 60), 2) AS gpm,
	ROUND(AVG(ppv.dmg_dealt) / AVG(ppv.total_gold), 2) AS ddpg
FROM picks_bans_prio_view AS ppv
INNER JOIN champion AS c ON
	c.id = ppv.pick_id
WHERE ppv.tournament_id = 7
GROUP BY c.name
ORDER BY c.name

SELECT
	p.nickname,
	ROUND(AVG(ppv.length_sec), 2) AS avg_length_sec,
	COUNT(ppv.pick_id) qty_games,
	SUM(CAST(ppv.winner AS INT)) AS qty_win,
	SUM(CASE WHEN side = 'blue' THEN 1 ELSE 0 END) qty_blue_side,
	SUM(CASE WHEN side = 'blue' AND ppv.winner THEN 1 ELSE 0 END) win_blue_side,
	SUM(CASE WHEN side = 'red' THEN 1 ELSE 0 END) qty_red_side,
	SUM(CASE WHEN side = 'red' AND ppv.winner THEN 1 ELSE 0 END) win_red_side,
	SUM(CASE WHEN ppv.is_blind THEN 1 ELSE 0 END) AS qty_blind,
	SUM(CASE WHEN ppv.is_blind AND ppv.winner THEN 1 ELSE 0 END) AS win_blind,
	SUM(CASE WHEN ppv.is_blind = false THEN 1 ELSE 0 END) AS qty_response,
	SUM(CASE WHEN ppv.is_blind = false AND ppv.winner THEN 1 ELSE 0 END) AS win_response,
	ROUND(AVG(ppv.kills), 2) AS avg_kills,
	ROUND(AVG(ppv.deaths), 2) AS avg_deaths,
	ROUND(AVG(ppv.assists), 2) AS avg_assists,
	ROUND((AVG(ppv.kills) + AVG(ppv.assists)) / AVG(ppv.deaths), 2) AS kda,
	ROUND(AVG(ppv.dmg_dealt) / (AVG(ppv.length_sec) / 60), 2) AS ddpm,
	ROUND(AVG(ppv.total_gold) / (AVG(ppv.length_sec) / 60), 2) AS gpm,
	ROUND(AVG(ppv.dmg_dealt) / AVG(ppv.total_gold), 2) AS ddpg
FROM picks_bans_prio_view AS ppv
INNER JOIN player AS p ON
	p.id = ppv.player
WHERE ppv.tournament_id = 7
GROUP BY p.nickname
ORDER BY p.nickname
