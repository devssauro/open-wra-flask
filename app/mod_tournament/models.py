from enum import IntEnum, unique

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy_serializer import SerializerMixin

from app.mod_team.models import Role
from db_config import Base


@unique
class Drake(IntEnum):
    cloud = 1
    mountain = 2
    infernal = 3
    ocean = 4


class Tournament(Base, SerializerMixin):
    __tablename__ = "tournament"

    def __init__(
        self,
        name,
        tag,
        region,
        start_date,
        end_date,
        split,
        phases: list | str,
        female_only: bool = False,
    ):
        self.name = name
        self.tag = tag
        self.region = region
        self.start_date = start_date
        self.end_date = end_date
        self.split = split
        if isinstance(phases, str):
            phases = phases.split(",")
        self.phases = phases
        self.female_only = female_only

    name = Column(String)
    tag = Column(String)
    region = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    split = Column(Integer)
    phases = Column(ARRAY(String))
    female_only = Column(Boolean, default=False)


class TournamentTeam(Base, SerializerMixin):
    __tablename__ = "tournament_team"

    def __init__(self, tournament_id, team_id, entry_phase):
        self.tournament_id = tournament_id
        self.team_id = team_id
        self.entry_phase = entry_phase

    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    team_id = Column(Integer, ForeignKey("team.id"))
    entry_phase = Column(String)
    players = relationship(
        "Player", secondary="tournament_lineup", backref=backref("lineups", lazy="dynamic")
    )


class TournamentLineup(Base, SerializerMixin):

    __tablename__ = "tournament_lineup"

    def __init__(self, tournament_id, team_id, entry_phase):
        self.tournament_id = tournament_id
        self.team_id = team_id
        self.entry_phase = entry_phase

    tournament_team_id = Column(Integer, ForeignKey("tournament_team.id"))
    player_id = Column(Integer, ForeignKey("player.id"))


class Champion(Base, SerializerMixin):
    __tablename__ = "champion"

    def __int__(self, name, avatar_url):
        self.datetime = name
        self.phase = avatar_url

    name = Column(String)


class Matchup(Base, SerializerMixin):
    __tablename__ = "matchup"

    def __int__(self, datetime, phase, mvp, team1, team2):
        self.datetime = datetime
        self.phase = phase
        self.mvp_id = mvp
        self.team1_id = team1
        self.team2_id = team2

    phase = Column(String)
    datetime = Column(DateTime)
    mvp_id = Column(Integer, ForeignKey("player.id"))
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    team1_id = Column(Integer, ForeignKey("team.id"))
    team2_id = Column(Integer, ForeignKey("team.id"))
    vod_link = Column(String)

    maps = relationship("MatchupMap", back_populates="matchup")


# Gold
# early 5 min
# mid 10 min
# late 15 min


class MatchupMap(Base, SerializerMixin):
    __tablename__ = "matchup_map"

    def __int__(
        self,
        matchup_id,
        map_number,
        patch,
        blue_side,
        red_side,
        length,
        winner,
        winner_side,
        tournament_id,
        vod_link,
        blue_baron_pick,
        blue_jungle_pick,
        blue_mid_pick,
        blue_dragon_pick,
        blue_sup_pick,
        red_baron_pick,
        red_jungle_pick,
        red_mid_pick,
        red_dragon_pick,
        red_sup_pick,
        blue_ban_1,
        blue_ban_2,
        blue_ban_3,
        blue_ban_4,
        blue_ban_5,
        red_ban_1,
        red_ban_2,
        red_ban_3,
        red_ban_4,
        red_ban_5,
        blue_pick_1,
        blue_pick_2,
        blue_pick_3,
        blue_pick_4,
        blue_pick_5,
        red_pick_1,
        red_pick_2,
        red_pick_3,
        red_pick_4,
        red_pick_5,
        blue_baron_kills,
        blue_jungle_kills,
        blue_mid_kills,
        blue_dragon_kills,
        blue_sup_kills,
        red_baron_kills,
        red_jungle_kills,
        red_mid_kills,
        red_dragon_kills,
        red_sup_kills,
        blue_baron_deaths,
        blue_jungle_deaths,
        blue_mid_deaths,
        blue_dragon_deaths,
        blue_sup_deaths,
        red_baron_deaths,
        red_jungle_deaths,
        red_mid_deaths,
        red_dragon_deaths,
        red_sup_deaths,
        blue_baron_assists,
        blue_jungle_assists,
        blue_mid_assists,
        blue_dragon_assists,
        blue_sup_assists,
        red_baron_assists,
        red_jungle_assists,
        red_mid_assists,
        red_dragon_assists,
        red_sup_assists,
        blue_baron_dmg_taken,
        blue_jungle_dmg_taken,
        blue_mid_dmg_taken,
        blue_dragon_dmg_taken,
        blue_sup_dmg_taken,
        red_baron_dmg_taken,
        red_jungle_dmg_taken,
        red_mid_dmg_taken,
        red_dragon_dmg_taken,
        red_sup_dmg_taken,
        blue_baron_dmg_dealt,
        blue_jungle_dmg_dealt,
        blue_mid_dmg_dealt,
        blue_dragon_dmg_dealt,
        blue_sup_dmg_dealt,
        red_baron_dmg_dealt,
        red_jungle_dmg_dealt,
        red_mid_dmg_dealt,
        red_dragon_dmg_dealt,
        red_sup_dmg_dealt,
        blue_baron_total_gold,
        blue_jungle_total_gold,
        blue_mid_total_gold,
        blue_dragon_total_gold,
        blue_sup_total_gold,
        red_baron_total_gold,
        red_jungle_total_gold,
        red_mid_total_gold,
        red_dragon_total_gold,
        red_sup_total_gold,
        blue_baron_player,
        blue_jungle_player,
        blue_mid_player,
        blue_dragon_player,
        blue_sup_player,
        red_baron_player,
        red_jungle_player,
        red_mid_player,
        red_dragon_player,
        red_sup_player,
        team_first_blood,
        player_first_blood,
        player_first_death,
        place_first_blood,
        team_first_herald,
        first_herald_teamfight,
        first_herald_stealed,
        first_herald_route,
        team_second_herald,
        second_herald_teamfight,
        second_herald_stealed,
        second_herald_route,
        team_first_tower,
        first_tower_route,
        first_tower_herald,
        team_first_drake,
        first_drake_type,
        first_drake_teamfight,
        first_drake_stealed,
        team_second_drake,
        second_drake_type,
        third_drake_teamfight,
        second_drake_stealed,
        team_third_drake,
        third_drake_type,
        second_drake_teamfight,
        third_drake_stealed,
        blue_turrets_destroyed,
        red_turrets_destroyed,
    ):

        self.vod_link = vod_link
        self.matchup_id = matchup_id
        self.map_number = map_number
        self.tournament_id = tournament_id
        self.patch = patch
        self.blue_side = blue_side
        self.red_side = red_side
        self.length = length
        self.winner = winner
        self.winner_side = winner_side
        self.blue_baron_pick = blue_baron_pick
        self.blue_jungle_pick = blue_jungle_pick
        self.blue_mid_pick = blue_mid_pick
        self.blue_dragon_pick = blue_dragon_pick
        self.blue_sup_pick = blue_sup_pick
        self.red_baron_pick = red_baron_pick
        self.red_jungle_pick = red_jungle_pick
        self.red_mid_pick = red_mid_pick
        self.red_dragon_pick = red_dragon_pick
        self.red_sup_pick = red_sup_pick
        self.blue_ban_1 = blue_ban_1
        self.blue_ban_2 = blue_ban_2
        self.blue_ban_3 = blue_ban_3
        self.blue_ban_4 = blue_ban_4
        self.blue_ban_5 = blue_ban_5
        self.red_ban_1 = red_ban_1
        self.red_ban_2 = red_ban_2
        self.red_ban_3 = red_ban_3
        self.red_ban_4 = red_ban_4
        self.red_ban_5 = red_ban_5
        self.blue_pick_1 = blue_pick_1
        self.blue_pick_2 = blue_pick_2
        self.blue_pick_3 = blue_pick_3
        self.blue_pick_4 = blue_pick_4
        self.blue_pick_5 = blue_pick_5
        self.red_pick_1 = red_pick_1
        self.red_pick_2 = red_pick_2
        self.red_pick_3 = red_pick_3
        self.red_pick_4 = red_pick_4
        self.red_pick_5 = red_pick_5
        self.blue_baron_player = blue_baron_player
        self.blue_jungle_player = blue_jungle_player
        self.blue_mid_player = blue_mid_player
        self.blue_dragon_player = blue_dragon_player
        self.blue_sup_player = blue_sup_player
        self.red_baron_player = red_baron_player
        self.red_jungle_player = red_jungle_player
        self.red_mid_player = red_mid_player
        self.red_dragon_player = red_dragon_player
        self.red_sup_player = red_sup_player
        self.blue_baron_kills = blue_baron_kills
        self.blue_jungle_kills = blue_jungle_kills
        self.blue_mid_kills = blue_mid_kills
        self.blue_dragon_kills = blue_dragon_kills
        self.blue_sup_kills = blue_sup_kills
        self.red_baron_kills = red_baron_kills
        self.red_jungle_kills = red_jungle_kills
        self.red_mid_kills = red_mid_kills
        self.red_dragon_kills = red_dragon_kills
        self.red_sup_kills = red_sup_kills
        self.blue_baron_deaths = blue_baron_deaths
        self.blue_jungle_deaths = blue_jungle_deaths
        self.blue_mid_deaths = blue_mid_deaths
        self.blue_dragon_deaths = blue_dragon_deaths
        self.blue_sup_deaths = blue_sup_deaths
        self.red_baron_deaths = red_baron_deaths
        self.red_jungle_deaths = red_jungle_deaths
        self.red_mid_deaths = red_mid_deaths
        self.red_dragon_deaths = red_dragon_deaths
        self.red_sup_deaths = red_sup_deaths
        self.blue_baron_assists = blue_baron_assists
        self.blue_jungle_assists = blue_jungle_assists
        self.blue_mid_assists = blue_mid_assists
        self.blue_dragon_assists = blue_dragon_assists
        self.blue_sup_assists = blue_sup_assists
        self.red_baron_assists = red_baron_assists
        self.red_jungle_assists = red_jungle_assists
        self.red_mid_assists = red_mid_assists
        self.red_dragon_assists = red_dragon_assists
        self.red_sup_assists = red_sup_assists
        self.blue_baron_dmg_taken = blue_baron_dmg_taken
        self.blue_jungle_dmg_taken = blue_jungle_dmg_taken
        self.blue_mid_dmg_taken = blue_mid_dmg_taken
        self.blue_dragon_dmg_taken = blue_dragon_dmg_taken
        self.blue_sup_dmg_taken = blue_sup_dmg_taken
        self.red_baron_dmg_taken = red_baron_dmg_taken
        self.red_jungle_dmg_taken = red_jungle_dmg_taken
        self.red_mid_dmg_taken = red_mid_dmg_taken
        self.red_dragon_dmg_taken = red_dragon_dmg_taken
        self.red_sup_dmg_taken = red_sup_dmg_taken
        self.blue_baron_dmg_dealt = blue_baron_dmg_dealt
        self.blue_jungle_dmg_dealt = blue_jungle_dmg_dealt
        self.blue_mid_dmg_dealt = blue_mid_dmg_dealt
        self.blue_dragon_dmg_dealt = blue_dragon_dmg_dealt
        self.blue_sup_dmg_dealt = blue_sup_dmg_dealt
        self.red_baron_dmg_dealt = red_baron_dmg_dealt
        self.red_jungle_dmg_dealt = red_jungle_dmg_dealt
        self.red_mid_dmg_dealt = red_mid_dmg_dealt
        self.red_dragon_dmg_dealt = red_dragon_dmg_dealt
        self.red_sup_dmg_dealt = red_sup_dmg_dealt
        self.blue_baron_total_gold = blue_baron_total_gold
        self.blue_jungle_total_gold = blue_jungle_total_gold
        self.blue_mid_total_gold = blue_mid_total_gold
        self.blue_dragon_total_gold = blue_dragon_total_gold
        self.blue_sup_total_gold = blue_sup_total_gold
        self.red_baron_total_gold = red_baron_total_gold
        self.red_jungle_total_gold = red_jungle_total_gold
        self.red_mid_total_gold = red_mid_total_gold
        self.red_dragon_total_gold = red_dragon_total_gold
        self.red_sup_total_gold = red_sup_total_gold
        self.team_first_blood = team_first_blood
        self.player_first_blood = player_first_blood
        self.player_first_death = player_first_death
        self.place_first_blood = place_first_blood
        self.team_first_herald = team_first_herald
        self.first_herald_teamfight = first_herald_teamfight
        self.first_herald_stealed = first_herald_stealed
        self.first_herald_route = first_herald_route
        self.team_second_herald = team_second_herald
        self.second_herald_teamfight = second_herald_teamfight
        self.second_herald_stealed = second_herald_stealed
        self.second_herald_route = second_herald_route
        self.team_first_drake = team_first_drake
        self.first_drake_teamfight = first_drake_teamfight
        self.first_drake_stealed = first_drake_stealed
        self.first_drake_type = first_drake_type
        self.team_second_drake = team_second_drake
        self.second_drake_teamfight = second_drake_teamfight
        self.second_drake_stealed = second_drake_stealed
        self.second_drake_type = second_drake_type
        self.team_third_drake = team_third_drake
        self.third_drake_teamfight = third_drake_teamfight
        self.third_drake_stealed = third_drake_stealed
        self.third_drake_type = third_drake_type
        self.team_first_tower = team_first_tower
        self.first_tower_route = first_tower_route
        self.first_tower_herald = first_tower_herald
        self.blue_turrets_destroyed = blue_turrets_destroyed
        self.red_turrets_destroyed = red_turrets_destroyed

    def update(self, data: dict):
        self.__int__(**data)  # type: ignore

    id = Column(Integer, primary_key=True, autoincrement=True)
    matchup_id = Column(Integer, ForeignKey("matchup.id"))
    matchup = relationship("Matchup", back_populates="maps")
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    vod_link = Column(String)
    map_number = Column(Integer)
    patch = Column(String)
    blue_side = Column(Integer, ForeignKey("team.id"))
    red_side = Column(Integer, ForeignKey("team.id"))
    length = Column(String)
    winner = Column(Integer, ForeignKey("team.id"))
    winner_side = Column(String)
    blue_ban_1 = Column(Integer, ForeignKey("champion.id"))
    red_ban_1 = Column(Integer, ForeignKey("champion.id"))
    blue_ban_2 = Column(Integer, ForeignKey("champion.id"))
    red_ban_2 = Column(Integer, ForeignKey("champion.id"))
    blue_ban_3 = Column(Integer, ForeignKey("champion.id"))
    red_ban_3 = Column(Integer, ForeignKey("champion.id"))
    blue_pick_1 = Column(Integer, ForeignKey("champion.id"))
    red_pick_1 = Column(Integer, ForeignKey("champion.id"))
    red_pick_2 = Column(Integer, ForeignKey("champion.id"))
    blue_pick_2 = Column(Integer, ForeignKey("champion.id"))
    blue_pick_3 = Column(Integer, ForeignKey("champion.id"))
    red_pick_3 = Column(Integer, ForeignKey("champion.id"))
    blue_ban_4 = Column(Integer, ForeignKey("champion.id"))
    red_ban_4 = Column(Integer, ForeignKey("champion.id"))
    blue_ban_5 = Column(Integer, ForeignKey("champion.id"))
    red_ban_5 = Column(Integer, ForeignKey("champion.id"))
    red_pick_4 = Column(Integer, ForeignKey("champion.id"))
    blue_pick_4 = Column(Integer, ForeignKey("champion.id"))
    blue_pick_5 = Column(Integer, ForeignKey("champion.id"))
    red_pick_5 = Column(Integer, ForeignKey("champion.id"))
    blue_baron_pick = Column(Integer, ForeignKey("champion.id"))
    blue_jungle_pick = Column(Integer, ForeignKey("champion.id"))
    blue_mid_pick = Column(Integer, ForeignKey("champion.id"))
    blue_dragon_pick = Column(Integer, ForeignKey("champion.id"))
    blue_sup_pick = Column(Integer, ForeignKey("champion.id"))
    red_baron_pick = Column(Integer, ForeignKey("champion.id"))
    red_jungle_pick = Column(Integer, ForeignKey("champion.id"))
    red_mid_pick = Column(Integer, ForeignKey("champion.id"))
    red_dragon_pick = Column(Integer, ForeignKey("champion.id"))
    red_sup_pick = Column(Integer, ForeignKey("champion.id"))
    blue_baron_player = Column(Integer, ForeignKey("player.id"))
    blue_jungle_player = Column(Integer, ForeignKey("player.id"))
    blue_mid_player = Column(Integer, ForeignKey("player.id"))
    blue_dragon_player = Column(Integer, ForeignKey("player.id"))
    blue_sup_player = Column(Integer, ForeignKey("player.id"))
    red_baron_player = Column(Integer, ForeignKey("player.id"))
    red_mid_player = Column(Integer, ForeignKey("player.id"))
    red_jungle_player = Column(Integer, ForeignKey("player.id"))
    red_dragon_player = Column(Integer, ForeignKey("player.id"))
    red_sup_player = Column(Integer, ForeignKey("player.id"))
    blue_baron_kills = Column(Integer, default=0)
    blue_jungle_kills = Column(Integer, default=0)
    blue_mid_kills = Column(Integer, default=0)
    blue_dragon_kills = Column(Integer, default=0)
    blue_sup_kills = Column(Integer, default=0)
    red_baron_kills = Column(Integer, default=0)
    red_jungle_kills = Column(Integer, default=0)
    red_mid_kills = Column(Integer, default=0)
    red_dragon_kills = Column(Integer, default=0)
    red_sup_kills = Column(Integer, default=0)
    blue_baron_deaths = Column(Integer, default=0)
    blue_jungle_deaths = Column(Integer, default=0)
    blue_mid_deaths = Column(Integer, default=0)
    blue_dragon_deaths = Column(Integer, default=0)
    blue_sup_deaths = Column(Integer, default=0)
    red_baron_deaths = Column(Integer, default=0)
    red_jungle_deaths = Column(Integer, default=0)
    red_mid_deaths = Column(Integer, default=0)
    red_dragon_deaths = Column(Integer, default=0)
    red_sup_deaths = Column(Integer, default=0)
    blue_baron_assists = Column(Integer, default=0)
    blue_jungle_assists = Column(Integer, default=0)
    blue_mid_assists = Column(Integer, default=0)
    blue_dragon_assists = Column(Integer, default=0)
    blue_sup_assists = Column(Integer, default=0)
    red_baron_assists = Column(Integer, default=0)
    red_jungle_assists = Column(Integer, default=0)
    red_mid_assists = Column(Integer, default=0)
    red_dragon_assists = Column(Integer, default=0)
    red_sup_assists = Column(Integer, default=0)
    blue_baron_dmg_taken = Column(Integer, default=0)
    blue_jungle_dmg_taken = Column(Integer, default=0)
    blue_mid_dmg_taken = Column(Integer, default=0)
    blue_dragon_dmg_taken = Column(Integer, default=0)
    blue_sup_dmg_taken = Column(Integer, default=0)
    red_baron_dmg_taken = Column(Integer, default=0)
    red_jungle_dmg_taken = Column(Integer, default=0)
    red_mid_dmg_taken = Column(Integer, default=0)
    red_dragon_dmg_taken = Column(Integer, default=0)
    red_sup_dmg_taken = Column(Integer, default=0)
    blue_baron_dmg_dealt = Column(Integer, default=0)
    blue_jungle_dmg_dealt = Column(Integer, default=0)
    blue_mid_dmg_dealt = Column(Integer, default=0)
    blue_dragon_dmg_dealt = Column(Integer, default=0)
    blue_sup_dmg_dealt = Column(Integer, default=0)
    red_baron_dmg_dealt = Column(Integer, default=0)
    red_jungle_dmg_dealt = Column(Integer, default=0)
    red_mid_dmg_dealt = Column(Integer, default=0)
    red_dragon_dmg_dealt = Column(Integer, default=0)
    red_sup_dmg_dealt = Column(Integer, default=0)
    blue_baron_total_gold = Column(Integer, default=0)
    blue_jungle_total_gold = Column(Integer, default=0)
    blue_mid_total_gold = Column(Integer, default=0)
    blue_dragon_total_gold = Column(Integer, default=0)
    blue_sup_total_gold = Column(Integer, default=0)
    red_baron_total_gold = Column(Integer, default=0)
    red_jungle_total_gold = Column(Integer, default=0)
    red_mid_total_gold = Column(Integer, default=0)
    red_dragon_total_gold = Column(Integer, default=0)
    red_sup_total_gold = Column(Integer, default=0)
    blue_turrets_destroyed = Column(Integer, default=0)
    red_turrets_destroyed = Column(Integer, default=0)
    team_first_blood = Column(Integer, ForeignKey("team.id"))
    player_first_blood = Column(Integer, ForeignKey("player.id"))
    player_first_death = Column(Integer, ForeignKey("player.id"))
    place_first_blood = Column(String)
    team_first_herald = Column(Integer, ForeignKey("team.id"))
    first_herald_teamfight = Column(Boolean, default=False)
    first_herald_stealed = Column(Boolean, default=False)
    first_herald_route = Column(String)
    team_second_herald = Column(Integer, ForeignKey("team.id"))
    second_herald_teamfight = Column(Boolean, default=False)
    second_herald_stealed = Column(Boolean, default=False)
    second_herald_route = Column(String)
    team_first_drake = Column(Integer, ForeignKey("team.id"))
    first_drake_teamfight = Column(Boolean, default=False)
    first_drake_stealed = Column(Boolean, default=False)
    first_drake_type = Column(String)
    team_second_drake = Column(Integer, ForeignKey("team.id"))
    second_drake_teamfight = Column(Boolean, default=False)
    second_drake_stealed = Column(Boolean, default=False)
    second_drake_type = Column(String)
    team_third_drake = Column(Integer, ForeignKey("team.id"))
    third_drake_teamfight = Column(Boolean, default=False)
    third_drake_stealed = Column(Boolean, default=False)
    third_drake_type = Column(String)
    team_first_tower = Column(Integer, ForeignKey("team.id"))
    first_tower_route = Column(Enum(Role))
    first_tower_herald = Column(Boolean, default=False)
