from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declared_attr

from app.exceptions import DraftIntegrityError
from app.mod_team.models import Role


class PicksBans:
    """All picks and bans from a matchup"""

    __abstract__ = True

    @declared_attr
    def blue_ban_1(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_ban_1(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_ban_2(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_ban_2(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_ban_3(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_ban_3(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_pick_1(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_pick_1(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_pick_2(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_pick_2(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_pick_3(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_pick_3(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_ban_4(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_ban_4(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_ban_5(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_ban_5(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_pick_4(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_pick_4(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def blue_pick_5(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    @declared_attr
    def red_pick_5(cls) -> int | Column:
        return Column(Integer, ForeignKey("champion.id"))

    def from_payload(self, **kwargs):
        _all_picks_bans = [kwargs[key] for key in kwargs if kwargs[key] is not None]
        if len(_all_picks_bans) != len(set(_all_picks_bans)):
            raise DraftIntegrityError("Cannot have redundant picks/bans")

        self.blue_ban_1 = kwargs.get("blue_ban_1")
        self.red_ban_1 = kwargs.get("red_ban_1")
        self.blue_ban_2 = kwargs.get("blue_ban_2")
        self.red_ban_2 = kwargs.get("red_ban_2")
        self.blue_ban_3 = kwargs.get("blue_ban_3")
        self.red_ban_3 = kwargs.get("red_ban_3")
        self.blue_pick_1 = kwargs.get("blue_pick_1")
        self.red_pick_1 = kwargs.get("red_pick_1")
        self.red_pick_2 = kwargs.get("red_pick_2")
        self.blue_pick_2 = kwargs.get("blue_pick_2")
        self.blue_pick_3 = kwargs.get("blue_pick_3")
        self.red_pick_3 = kwargs.get("red_pick_3")
        self.red_ban_4 = kwargs.get("red_ban_4")
        self.blue_ban_4 = kwargs.get("blue_ban_4")
        self.red_ban_5 = kwargs.get("red_ban_5")
        self.blue_ban_5 = kwargs.get("blue_ban_5")
        self.red_pick_4 = kwargs.get("red_pick_4")
        self.blue_pick_4 = kwargs.get("blue_pick_4")
        self.blue_pick_5 = kwargs.get("blue_pick_5")
        self.red_pick_5 = kwargs.get("red_pick_5")


class Players:
    @declared_attr
    def blue_baron_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def blue_jungle_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def blue_mid_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def blue_dragon_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def blue_sup_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def red_baron_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def red_mid_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def red_jungle_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def red_dragon_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def red_sup_player(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    def from_payload(self, **kwargs):
        self.blue_baron_player = kwargs.get("blue_baron_player")
        self.blue_jungle_player = kwargs.get("blue_jungle_player")
        self.blue_mid_player = kwargs.get("blue_mid_player")
        self.blue_dragon_player = kwargs.get("blue_dragon_player")
        self.blue_sup_player = kwargs.get("blue_sup_player")
        self.red_baron_player = kwargs.get("red_baron_player")
        self.red_jungle_player = kwargs.get("red_jungle_player")
        self.red_mid_player = kwargs.get("red_mid_player")
        self.red_dragon_player = kwargs.get("red_dragon_player")
        self.red_sup_player = kwargs.get("red_sup_player")


class KDA:
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

    def from_payload(self, **kwargs):
        self.blue_baron_kills = kwargs.get("blue_baron_kills")
        self.blue_jungle_kills = kwargs.get("blue_jungle_kills")
        self.blue_mid_kills = kwargs.get("blue_mid_kills")
        self.blue_dragon_kills = kwargs.get("blue_dragon_kills")
        self.blue_sup_kills = kwargs.get("blue_sup_kills")
        self.red_baron_kills = kwargs.get("red_baron_kills")
        self.red_jungle_kills = kwargs.get("red_jungle_kills")
        self.red_mid_kills = kwargs.get("red_mid_kills")
        self.red_dragon_kills = kwargs.get("red_dragon_kills")
        self.red_sup_kills = kwargs.get("red_sup_kills")
        self.blue_baron_deaths = kwargs.get("blue_baron_deaths")
        self.blue_jungle_deaths = kwargs.get("blue_jungle_deaths")
        self.blue_mid_deaths = kwargs.get("blue_mid_deaths")
        self.blue_dragon_deaths = kwargs.get("blue_dragon_deaths")
        self.blue_sup_deaths = kwargs.get("blue_sup_deaths")
        self.red_baron_deaths = kwargs.get("red_baron_deaths")
        self.red_jungle_deaths = kwargs.get("red_jungle_deaths")
        self.red_mid_deaths = kwargs.get("red_mid_deaths")
        self.red_dragon_deaths = kwargs.get("red_dragon_deaths")
        self.red_sup_deaths = kwargs.get("red_sup_deaths")
        self.blue_baron_assists = kwargs.get("blue_baron_assists")
        self.blue_jungle_assists = kwargs.get("blue_jungle_assists")
        self.blue_mid_assists = kwargs.get("blue_mid_assists")
        self.blue_dragon_assists = kwargs.get("blue_dragon_assists")
        self.blue_sup_assists = kwargs.get("blue_sup_assists")
        self.red_baron_assists = kwargs.get("red_baron_assists")
        self.red_jungle_assists = kwargs.get("red_jungle_assists")
        self.red_mid_assists = kwargs.get("red_mid_assists")
        self.red_dragon_assists = kwargs.get("red_dragon_assists")
        self.red_sup_assists = kwargs.get("red_sup_assists")


class DamageTaken:
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

    def from_payload(self, **kwargs):
        self.blue_baron_dmg_taken = kwargs.get("blue_baron_dmg_taken")
        self.blue_jungle_dmg_taken = kwargs.get("blue_jungle_dmg_taken")
        self.blue_mid_dmg_taken = kwargs.get("blue_mid_dmg_taken")
        self.blue_dragon_dmg_taken = kwargs.get("blue_dragon_dmg_taken")
        self.blue_sup_dmg_taken = kwargs.get("blue_sup_dmg_taken")
        self.red_baron_dmg_taken = kwargs.get("red_baron_dmg_taken")
        self.red_jungle_dmg_taken = kwargs.get("red_jungle_dmg_taken")
        self.red_mid_dmg_taken = kwargs.get("red_mid_dmg_taken")
        self.red_dragon_dmg_taken = kwargs.get("red_dragon_dmg_taken")
        self.red_sup_dmg_taken = kwargs.get("red_sup_dmg_taken")


class DamageDealt:
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

    def from_payload(self, **kwargs):
        self.blue_baron_dmg_dealt = kwargs.get("blue_baron_dmg_dealt")
        self.blue_jungle_dmg_dealt = kwargs.get("blue_jungle_dmg_dealt")
        self.blue_mid_dmg_dealt = kwargs.get("blue_mid_dmg_dealt")
        self.blue_dragon_dmg_dealt = kwargs.get("blue_dragon_dmg_dealt")
        self.blue_sup_dmg_dealt = kwargs.get("blue_sup_dmg_dealt")
        self.red_baron_dmg_dealt = kwargs.get("red_baron_dmg_dealt")
        self.red_jungle_dmg_dealt = kwargs.get("red_jungle_dmg_dealt")
        self.red_mid_dmg_dealt = kwargs.get("red_mid_dmg_dealt")
        self.red_dragon_dmg_dealt = kwargs.get("red_dragon_dmg_dealt")
        self.red_sup_dmg_dealt = kwargs.get("red_sup_dmg_dealt")


class TotalGold:
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

    def from_payload(self, **kwargs):
        self.blue_baron_total_gold = kwargs.get("blue_baron_total_gold")
        self.blue_jungle_total_gold = kwargs.get("blue_jungle_total_gold")
        self.blue_mid_total_gold = kwargs.get("blue_mid_total_gold")
        self.blue_dragon_total_gold = kwargs.get("blue_dragon_total_gold")
        self.blue_sup_total_gold = kwargs.get("blue_sup_total_gold")
        self.red_baron_total_gold = kwargs.get("red_baron_total_gold")
        self.red_jungle_total_gold = kwargs.get("red_jungle_total_gold")
        self.red_mid_total_gold = kwargs.get("red_mid_total_gold")
        self.red_dragon_total_gold = kwargs.get("red_dragon_total_gold")
        self.red_sup_total_gold = kwargs.get("red_sup_total_gold")


class FirstBlood:
    @declared_attr
    def team_first_blood(cls) -> int | Column:
        return Column(Integer, ForeignKey("team.id"))

    @declared_attr
    def player_first_blood(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def player_first_death(cls) -> int | Column:
        return Column(Integer, ForeignKey("player.id"))

    place_first_blood = Column(String)

    def from_payload(self, **kwargs):
        self.team_first_blood = kwargs.get("team_first_blood")
        self.player_first_blood = kwargs.get("player_first_blood")
        self.player_first_death = kwargs.get("player_first_death")
        self.place_first_blood = kwargs.get("place_first_blood")


class FirstTower:
    @declared_attr
    def team_first_tower(cls):
        return Column(Integer, ForeignKey("team.id"))

    first_tower_route = Column(Enum(Role))
    first_tower_herald = Column(Boolean, default=False)

    def from_payload(self, **kwargs):
        self.team_first_tower = kwargs.get("team_first_tower")
        self.first_tower_route = kwargs.get("first_tower_route")
        self.first_tower_herald = kwargs.get("first_tower_herald")


class FirstHerald:
    """Fields that refers the first herald for a match

    Attributes:
        team_first_herald (int): Team's id that takes the herald
        first_herald_teamfight (bool): If there was a teamfight when the herald was taken
        first_herald_stealed (bool): If the herald was stealed
    """

    @declared_attr
    def team_first_herald(cls) -> int | Column:
        return Column(Integer, ForeignKey("team.id"))

    first_herald_teamfight = Column(Boolean, default=False)
    first_herald_stealed = Column(Boolean, default=False)
    first_herald_route = Column(String)

    def from_payload(self, **kwargs):
        self.team_first_herald = kwargs.get("team_first_herald")
        self.first_herald_teamfight = kwargs.get("first_herald_teamfight")
        self.first_herald_stealed = kwargs.get("first_herald_stealed")
        self.first_herald_route = kwargs.get("first_herald_route")


class SecondHerald:
    """Fields that refers the second herald for a match

    Attributes:
        team_second_herald (int): Team's id that takes the herald
        second_herald_teamfight (bool): If there was a teamfight when the herald was taken
        second_herald_stealed (bool): If the herald was stealed
    """

    @declared_attr
    def team_second_herald(cls):
        return Column(Integer, ForeignKey("team.id"))

    second_herald_teamfight = Column(Boolean, default=False)
    second_herald_stealed = Column(Boolean, default=False)
    second_herald_route = Column(String)

    def from_payload(self, **kwargs):
        self.team_second_herald = kwargs.get("team_second_herald")
        self.second_herald_teamfight = kwargs.get("second_herald_teamfight")
        self.second_herald_stealed = kwargs.get("second_herald_stealed")
        self.second_herald_route = kwargs.get("second_herald_route")


class FirstDrake:
    """Fields that refers the first drake for a match

    Attributes:
        team_first_drake (int): Team's id that takes the drake
        first_drake_teamfight (bool): If there was a teamfight when the drake was taken
        first_drake_stealed (bool): If the drake was stealed
    """

    @declared_attr
    def team_first_drake(cls) -> int | Column:
        return Column(Integer, ForeignKey("team.id"))

    first_drake_teamfight = Column(Boolean, default=False)
    first_drake_stealed = Column(Boolean, default=False)
    first_drake_type = Column(String)

    def from_payload(self, **kwargs):
        self.team_first_drake = kwargs.get("team_first_drake")
        self.first_drake_teamfight = kwargs.get("first_drake_teamfight")
        self.first_drake_stealed = kwargs.get("first_drake_stealed")
        self.first_drake_type = kwargs.get("first_drake_type")


class SecondDrake:
    """Fields that refers the second drake for a match

    Attributes:
        team_second_drake (int): Team's id that takes the drake
        second_drake_teamfight (bool): If there was a teamfight when the drake was taken
        second_drake_stealed (bool): If the drake was stealed
    """

    @declared_attr
    def team_second_drake(cls) -> int | Column:
        return Column(Integer, ForeignKey("team.id"))

    second_drake_teamfight = Column(Boolean, default=False)
    second_drake_stealed = Column(Boolean, default=False)
    second_drake_type = Column(String)

    def from_payload(self, **kwargs):
        self.team_second_drake = kwargs.get("team_second_drake")
        self.second_drake_teamfight = kwargs.get("second_drake_teamfight")
        self.second_drake_stealed = kwargs.get("second_drake_stealed")
        self.second_drake_type = kwargs.get("second_drake_type")


class ThirdDrake:
    """Fields that refers the third drake for a match

    Attributes:
        team_third_drake (int): Team's id that takes the drake
        third_drake_teamfight (bool): If there was a teamfight when the drake was taken
        third_drake_stealed (bool): If the drake was stealed
    """

    @declared_attr
    def team_third_drake(cls) -> int | Column:
        return Column(Integer, ForeignKey("team.id"))

    third_drake_teamfight = Column(Boolean, default=False)
    third_drake_stealed = Column(Boolean, default=False)
    third_drake_type = Column(String)

    def from_payload(self, **kwargs):
        self.team_third_drake = kwargs.get("team_third_drake")
        self.third_drake_teamfight = kwargs.get("third_drake_teamfight")
        self.third_drake_stealed = kwargs.get("third_drake_stealed")
        self.third_drake_type = kwargs.get("third_drake_type")
