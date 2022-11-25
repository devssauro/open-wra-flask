from sqlalchemy import Boolean, Column, Enum, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import declarative_mixin

from app.exceptions import DraftIntegrityError, LineupIntegrityError
from app.mod_team.models import Role

SIDES = ("blue", "red")
ROLES = ("baron", "jungle", "mid", "dragon", "sup")
ALL_PICKS_BANS = tuple(
    f"{side}_{p_b}_{position}"
    for position in range(1, 6)
    for side in SIDES
    for p_b in ("pick", "ban")
)
ALL_PICKS = tuple(f"{side}_{role}_pick" for role in ROLES for side in SIDES)
ALL_PLAYERS = tuple(f"{side}_{role}_player" for role in ROLES for side in SIDES)
BLUE_DRAFT = tuple(f"blue_{role}_pick" for role in ROLES)
RED_DRAFT = tuple(f"red_{role}_pick" for role in ROLES)
ALL_BLUE_PICKS = tuple(f"blue_pick_{position}" for position in range(1, 6))
ALL_RED_PICKS = tuple(f"red_pick_{position}" for position in range(1, 6))


@declarative_mixin
class PicksBans:
    """All picks and bans from a matchup"""

    def __init__(
        self,
        blue_ban_1=None,
        red_ban_1=None,
        blue_ban_2=None,
        red_ban_2=None,
        blue_ban_3=None,
        red_ban_3=None,
        blue_pick_1=None,
        red_pick_1=None,
        red_pick_2=None,
        blue_pick_2=None,
        blue_pick_3=None,
        red_pick_3=None,
        red_ban_4=None,
        blue_ban_4=None,
        red_ban_5=None,
        blue_ban_5=None,
        red_pick_4=None,
        blue_pick_4=None,
        blue_pick_5=None,
        red_pick_5=None,
    ):
        self._blue_ban_1 = blue_ban_1
        self._red_ban_1 = red_ban_1
        self._blue_ban_2 = blue_ban_2
        self._red_ban_2 = red_ban_2
        self._blue_ban_3 = blue_ban_3
        self._red_ban_3 = red_ban_3
        self._blue_pick_1 = blue_pick_1
        self._red_pick_1 = red_pick_1
        self._red_pick_2 = red_pick_2
        self._blue_pick_2 = blue_pick_2
        self._blue_pick_3 = blue_pick_3
        self._red_pick_2 = red_pick_3
        self._red_pick_3 = red_ban_4
        self._blue_ban_4 = blue_ban_4
        self._red_ban_4 = red_ban_5
        self._blue_ban_5 = blue_ban_5
        self._red_ban_5 = red_ban_5
        self._red_pick_4 = red_pick_4
        self._blue_pick_4 = blue_pick_4
        self._blue_pick_5 = blue_pick_5
        self._red_pick_5 = red_pick_5

    __table_args__ = tuple(
        ForeignKeyConstraint(ALL_PICKS_BANS, ["champion.id" for i in range(20)])
    )

    blue_ban_1 = Column("blue_ban_1", Integer)
    red_ban_1 = Column("red_ban_1", Integer)
    blue_ban_2 = Column("blue_ban_2", Integer)
    red_ban_2 = Column("red_ban_2", Integer)
    blue_ban_3 = Column("blue_ban_3", Integer)
    red_ban_3 = Column("red_ban_3", Integer)
    blue_pick_1 = Column("blue_pick_1", Integer)
    red_pick_1 = Column("red_pick_1", Integer)
    red_pick_2 = Column("red_pick_2", Integer)
    blue_pick_2 = Column("blue_pick_2", Integer)
    blue_pick_3 = Column("blue_pick_3", Integer)
    red_pick_3 = Column("red_pick_3", Integer)
    red_ban_4 = Column("red_ban_4", Integer)
    blue_ban_4 = Column("blue_ban_4", Integer)
    red_ban_5 = Column("red_ban_5", Integer)
    blue_ban_5 = Column("blue_ban_5", Integer)
    red_pick_4 = Column("red_pick_4", Integer)
    blue_pick_4 = Column("blue_pick_4", Integer)
    blue_pick_5 = Column("blue_pick_5", Integer)
    red_pick_5 = Column("red_pick_5", Integer)

    @staticmethod
    def from_payload(obj=None, **kwargs):
        if obj is None:
            obj = PicksBans()
        _all_picks_bans = [
            kwargs.get(key) for key in ALL_PICKS_BANS if kwargs.get(key) is not None
        ]
        if len(_all_picks_bans) != len(set(_all_picks_bans)):
            raise DraftIntegrityError("Cannot have redundant picks/bans")

        obj.blue_ban_1 = kwargs.get("blue_ban_1")
        obj.red_ban_1 = kwargs.get("red_ban_1")
        obj.blue_ban_2 = kwargs.get("blue_ban_2")
        obj.red_ban_2 = kwargs.get("red_ban_2")
        obj.blue_ban_3 = kwargs.get("blue_ban_3")
        obj.red_ban_3 = kwargs.get("red_ban_3")
        obj.blue_pick_1 = kwargs.get("blue_pick_1")
        obj.red_pick_1 = kwargs.get("red_pick_1")
        obj.red_pick_2 = kwargs.get("red_pick_2")
        obj.blue_pick_2 = kwargs.get("blue_pick_2")
        obj.blue_pick_3 = kwargs.get("blue_pick_3")
        obj.red_pick_3 = kwargs.get("red_pick_3")
        obj.red_ban_4 = kwargs.get("red_ban_4")
        obj.blue_ban_4 = kwargs.get("blue_ban_4")
        obj.red_ban_5 = kwargs.get("red_ban_5")
        obj.blue_ban_5 = kwargs.get("blue_ban_5")
        obj.red_pick_4 = kwargs.get("red_pick_4")
        obj.blue_pick_4 = kwargs.get("blue_pick_4")
        obj.blue_pick_5 = kwargs.get("blue_pick_5")
        obj.red_pick_5 = kwargs.get("red_pick_5")

        return obj


@declarative_mixin
class Draft(PicksBans):

    __table_args__ = tuple(ForeignKeyConstraint(ALL_PICKS, ["champion.id" for i in range(10)]))

    blue_baron_pick = Column(Integer)
    blue_jungle_pick = Column(Integer)
    blue_mid_pick = Column(Integer)
    blue_dragon_pick = Column(Integer)
    blue_sup_pick = Column(Integer)
    red_baron_pick = Column(Integer)
    red_mid_pick = Column(Integer)
    red_jungle_pick = Column(Integer)
    red_dragon_pick = Column(Integer)
    red_sup_pick = Column(Integer)

    @staticmethod
    def from_payload(obj=None, **kwargs):
        if obj is None:
            obj = Draft()

        PicksBans.from_payload(obj, **kwargs)

        all_picks = [kwargs.get(key) for key in ALL_PICKS if kwargs.get(key) is not None]
        blue_picks = [kwargs.get(key) for key in ALL_BLUE_PICKS if kwargs.get(key) is not None]
        red_picks = [kwargs.get(key) for key in ALL_RED_PICKS if kwargs.get(key) is not None]
        if len(all_picks) != len(set(all_picks)):
            raise DraftIntegrityError("A champion can't stay in two positions at the same time")

        for pick in BLUE_DRAFT:
            if kwargs.get(pick) not in blue_picks:
                raise DraftIntegrityError(
                    "An unselected champion from blue side cannot be used to be played"
                )

        for pick in RED_DRAFT:
            if kwargs.get(pick) not in red_picks:
                raise DraftIntegrityError(
                    "An unselected champion from red side cannot be used to be played"
                )

        obj.blue_baron_pick = kwargs.get("blue_baron_pick")
        obj.blue_jungle_pick = kwargs.get("blue_jungle_pick")
        obj.blue_mid_pick = kwargs.get("blue_mid_pick")
        obj.blue_dragon_pick = kwargs.get("blue_dragon_pick")
        obj.blue_sup_pick = kwargs.get("blue_sup_pick")
        obj.red_baron_pick = kwargs.get("red_baron_pick")
        obj.red_jungle_pick = kwargs.get("red_jungle_pick")
        obj.red_mid_pick = kwargs.get("red_mid_pick")
        obj.red_dragon_pick = kwargs.get("red_dragon_pick")
        obj.red_sup_pick = kwargs.get("red_sup_pick")

        return obj


@declarative_mixin
class Players:

    __table_args__ = tuple(ForeignKeyConstraint(ALL_PLAYERS, ["player.id" for i in range(10)]))

    blue_baron_player = Column(Integer)
    blue_jungle_player = Column(Integer)
    blue_mid_player = Column(Integer)
    blue_dragon_player = Column(Integer)
    blue_sup_player = Column(Integer)
    red_baron_player = Column(Integer)
    red_mid_player = Column(Integer)
    red_jungle_player = Column(Integer)
    red_dragon_player = Column(Integer)
    red_sup_player = Column(Integer)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = Players()
        _all_players = [kwargs.get(key) for key in ALL_PLAYERS if kwargs.get(key) is not None]
        if len(_all_players) != len(set(_all_players)):
            raise LineupIntegrityError("A player can't stay in two positions at the same time")
        obj.blue_baron_player = kwargs.get("blue_baron_player")
        obj.blue_jungle_player = kwargs.get("blue_jungle_player")
        obj.blue_mid_player = kwargs.get("blue_mid_player")
        obj.blue_dragon_player = kwargs.get("blue_dragon_player")
        obj.blue_sup_player = kwargs.get("blue_sup_player")
        obj.red_baron_player = kwargs.get("red_baron_player")
        obj.red_jungle_player = kwargs.get("red_jungle_player")
        obj.red_mid_player = kwargs.get("red_mid_player")
        obj.red_dragon_player = kwargs.get("red_dragon_player")
        obj.red_sup_player = kwargs.get("red_sup_player")

        return obj


@declarative_mixin
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

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = KDA()

        obj.blue_baron_kills = kwargs.get("blue_baron_kills")
        obj.blue_jungle_kills = kwargs.get("blue_jungle_kills")
        obj.blue_mid_kills = kwargs.get("blue_mid_kills")
        obj.blue_dragon_kills = kwargs.get("blue_dragon_kills")
        obj.blue_sup_kills = kwargs.get("blue_sup_kills")
        obj.red_baron_kills = kwargs.get("red_baron_kills")
        obj.red_jungle_kills = kwargs.get("red_jungle_kills")
        obj.red_mid_kills = kwargs.get("red_mid_kills")
        obj.red_dragon_kills = kwargs.get("red_dragon_kills")
        obj.red_sup_kills = kwargs.get("red_sup_kills")
        obj.blue_baron_deaths = kwargs.get("blue_baron_deaths")
        obj.blue_jungle_deaths = kwargs.get("blue_jungle_deaths")
        obj.blue_mid_deaths = kwargs.get("blue_mid_deaths")
        obj.blue_dragon_deaths = kwargs.get("blue_dragon_deaths")
        obj.blue_sup_deaths = kwargs.get("blue_sup_deaths")
        obj.red_baron_deaths = kwargs.get("red_baron_deaths")
        obj.red_jungle_deaths = kwargs.get("red_jungle_deaths")
        obj.red_mid_deaths = kwargs.get("red_mid_deaths")
        obj.red_dragon_deaths = kwargs.get("red_dragon_deaths")
        obj.red_sup_deaths = kwargs.get("red_sup_deaths")
        obj.blue_baron_assists = kwargs.get("blue_baron_assists")
        obj.blue_jungle_assists = kwargs.get("blue_jungle_assists")
        obj.blue_mid_assists = kwargs.get("blue_mid_assists")
        obj.blue_dragon_assists = kwargs.get("blue_dragon_assists")
        obj.blue_sup_assists = kwargs.get("blue_sup_assists")
        obj.red_baron_assists = kwargs.get("red_baron_assists")
        obj.red_jungle_assists = kwargs.get("red_jungle_assists")
        obj.red_mid_assists = kwargs.get("red_mid_assists")
        obj.red_dragon_assists = kwargs.get("red_dragon_assists")
        obj.red_sup_assists = kwargs.get("red_sup_assists")


@declarative_mixin
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

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = DamageTaken()
        obj.blue_baron_dmg_taken = kwargs.get("blue_baron_dmg_taken")
        obj.blue_jungle_dmg_taken = kwargs.get("blue_jungle_dmg_taken")
        obj.blue_mid_dmg_taken = kwargs.get("blue_mid_dmg_taken")
        obj.blue_dragon_dmg_taken = kwargs.get("blue_dragon_dmg_taken")
        obj.blue_sup_dmg_taken = kwargs.get("blue_sup_dmg_taken")
        obj.red_baron_dmg_taken = kwargs.get("red_baron_dmg_taken")
        obj.red_jungle_dmg_taken = kwargs.get("red_jungle_dmg_taken")
        obj.red_mid_dmg_taken = kwargs.get("red_mid_dmg_taken")
        obj.red_dragon_dmg_taken = kwargs.get("red_dragon_dmg_taken")
        obj.red_sup_dmg_taken = kwargs.get("red_sup_dmg_taken")


@declarative_mixin
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

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = DamageDealt()
        obj.blue_baron_dmg_dealt = kwargs.get("blue_baron_dmg_dealt")
        obj.blue_jungle_dmg_dealt = kwargs.get("blue_jungle_dmg_dealt")
        obj.blue_mid_dmg_dealt = kwargs.get("blue_mid_dmg_dealt")
        obj.blue_dragon_dmg_dealt = kwargs.get("blue_dragon_dmg_dealt")
        obj.blue_sup_dmg_dealt = kwargs.get("blue_sup_dmg_dealt")
        obj.red_baron_dmg_dealt = kwargs.get("red_baron_dmg_dealt")
        obj.red_jungle_dmg_dealt = kwargs.get("red_jungle_dmg_dealt")
        obj.red_mid_dmg_dealt = kwargs.get("red_mid_dmg_dealt")
        obj.red_dragon_dmg_dealt = kwargs.get("red_dragon_dmg_dealt")
        obj.red_sup_dmg_dealt = kwargs.get("red_sup_dmg_dealt")


@declarative_mixin
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

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = TotalGold()
        obj.blue_baron_total_gold = kwargs.get("blue_baron_total_gold")
        obj.blue_jungle_total_gold = kwargs.get("blue_jungle_total_gold")
        obj.blue_mid_total_gold = kwargs.get("blue_mid_total_gold")
        obj.blue_dragon_total_gold = kwargs.get("blue_dragon_total_gold")
        obj.blue_sup_total_gold = kwargs.get("blue_sup_total_gold")
        obj.red_baron_total_gold = kwargs.get("red_baron_total_gold")
        obj.red_jungle_total_gold = kwargs.get("red_jungle_total_gold")
        obj.red_mid_total_gold = kwargs.get("red_mid_total_gold")
        obj.red_dragon_total_gold = kwargs.get("red_dragon_total_gold")
        obj.red_sup_total_gold = kwargs.get("red_sup_total_gold")


@declarative_mixin
class FirstBlood:

    __table_args__ = tuple(
        ForeignKeyConstraint(
            ("team_first_blood", "player_first_blood", "player_first_death"),
            ("team.id", "player.id", "player.id"),
        )
    )

    team_first_blood = Column(Integer)
    player_first_blood = Column(Integer)
    player_first_death = Column(Integer)
    place_first_blood = Column(String)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstBlood()
        obj.team_first_blood = kwargs.get("team_first_blood")
        obj.player_first_blood = kwargs.get("player_first_blood")
        obj.player_first_death = kwargs.get("player_first_death")
        obj.place_first_blood = kwargs.get("place_first_blood")


@declarative_mixin
class FirstTower:

    __table_args__ = tuple(
        ForeignKeyConstraint(
            tuple(["team_first_tower"]),
            tuple(["team.id"]),
        )
    )

    team_first_tower = Column(Integer)
    first_tower_route = Column(Enum(Role))
    first_tower_herald = Column(Boolean, default=False)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstTower()
        obj.team_first_tower = kwargs.get("team_first_tower")
        obj.first_tower_route = kwargs.get("first_tower_route")
        obj.first_tower_herald = kwargs.get("first_tower_herald")


@declarative_mixin
class FirstHerald:
    """Fields that refers the first herald for a match

    Attributes:
        team_first_herald (int): Team's id that takes the herald
        first_herald_teamfight (bool): If there was a teamfight when the herald was taken
        first_herald_stealed (bool): If the herald was stealed
    """

    __table_args__ = tuple(
        ForeignKeyConstraint(
            tuple(["team_first_herald"]),
            tuple(["team.id"]),
        )
    )

    team_first_herald = Column(Integer)
    first_herald_teamfight = Column(Boolean, default=False)
    first_herald_stealed = Column(Boolean, default=False)
    first_herald_route = Column(String)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstHerald()
        obj.team_first_herald = kwargs.get("team_first_herald")
        obj.first_herald_teamfight = kwargs.get("first_herald_teamfight")
        obj.first_herald_stealed = kwargs.get("first_herald_stealed")
        obj.first_herald_route = kwargs.get("first_herald_route")


@declarative_mixin
class SecondHerald:
    """Fields that refers the second herald for a match

    Attributes:
        team_second_herald (int): Team's id that takes the herald
        second_herald_teamfight (bool): If there was a teamfight when the herald was taken
        second_herald_stealed (bool): If the herald was stealed
    """

    __table_args__ = tuple(
        ForeignKeyConstraint(
            tuple(["team_second_herald"]),
            tuple(["team.id"]),
        )
    )

    team_second_herald = Column(Integer)
    second_herald_teamfight = Column(Boolean, default=False)
    second_herald_stealed = Column(Boolean, default=False)
    second_herald_route = Column(String)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = SecondHerald()
        obj.team_second_herald = kwargs.get("team_second_herald")
        obj.second_herald_teamfight = kwargs.get("second_herald_teamfight")
        obj.second_herald_stealed = kwargs.get("second_herald_stealed")
        obj.second_herald_route = kwargs.get("second_herald_route")


@declarative_mixin
class FirstDrake:
    """Fields that refers the first drake for a match

    Attributes:
        team_first_drake (int): Team's id that takes the drake
        first_drake_teamfight (bool): If there was a teamfight when the drake was taken
        first_drake_stealed (bool): If the drake was stealed
    """

    __table_args__ = tuple(
        ForeignKeyConstraint(
            tuple(["team_first_drake"]),
            tuple(["team.id"]),
        )
    )

    team_first_drake = Column(Integer)
    first_drake_teamfight = Column(Boolean, default=False)
    first_drake_stealed = Column(Boolean, default=False)
    first_drake_type = Column(String)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstDrake()
        obj.team_first_drake = kwargs.get("team_first_drake")
        obj.first_drake_teamfight = kwargs.get("first_drake_teamfight")
        obj.first_drake_stealed = kwargs.get("first_drake_stealed")
        obj.first_drake_type = kwargs.get("first_drake_type")


@declarative_mixin
class SecondDrake:
    """Fields that refers the second drake for a match

    Attributes:
        team_second_drake (int): Team's id that takes the drake
        second_drake_teamfight (bool): If there was a teamfight when the drake was taken
        second_drake_stealed (bool): If the drake was stealed
    """

    __table_args__ = tuple(
        ForeignKeyConstraint(
            tuple(["team_second_drake"]),
            tuple(["team.id"]),
        )
    )

    team_second_drake = Column(Integer)
    second_drake_teamfight = Column(Boolean, default=False)
    second_drake_stealed = Column(Boolean, default=False)
    second_drake_type = Column(String)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = SecondDrake()
        obj.team_second_drake = kwargs.get("team_second_drake")
        obj.second_drake_teamfight = kwargs.get("second_drake_teamfight")
        obj.second_drake_stealed = kwargs.get("second_drake_stealed")
        obj.second_drake_type = kwargs.get("second_drake_type")


@declarative_mixin
class ThirdDrake:
    """Fields that refers the third drake for a match

    Attributes:
        team_third_drake (int): Team's id that takes the drake
        third_drake_teamfight (bool): If there was a teamfight when the drake was taken
        third_drake_stealed (bool): If the drake was stealed
    """

    __table_args__ = tuple(
        ForeignKeyConstraint(
            tuple(["team_third_drake"]),
            tuple(["team.id"]),
        )
    )

    team_third_drake = Column(Integer)
    third_drake_teamfight = Column(Boolean, default=False)
    third_drake_stealed = Column(Boolean, default=False)
    third_drake_type = Column(String)

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = ThirdDrake()
        obj.team_third_drake = kwargs.get("team_third_drake")
        obj.third_drake_teamfight = kwargs.get("third_drake_teamfight")
        obj.third_drake_stealed = kwargs.get("third_drake_stealed")
        obj.third_drake_type = kwargs.get("third_drake_type")
