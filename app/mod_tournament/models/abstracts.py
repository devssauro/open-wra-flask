from typing import Optional

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column

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

    @declared_attr
    def __table_args__(cls):
        return tuple(
            ForeignKeyConstraint([pick_ban], ["champion.id"], f"matchup_map_{pick_ban}_fkey")
            for pick_ban in ALL_PICKS_BANS
        )

    blue_ban_1: Mapped[Optional[int]]
    red_ban_1: Mapped[Optional[int]]
    blue_ban_2: Mapped[Optional[int]]
    red_ban_2: Mapped[Optional[int]]
    blue_ban_3: Mapped[Optional[int]]
    red_ban_3: Mapped[Optional[int]]
    blue_pick_1: Mapped[Optional[int]]
    red_pick_1: Mapped[Optional[int]]
    red_pick_2: Mapped[Optional[int]]
    blue_pick_2: Mapped[Optional[int]]
    blue_pick_3: Mapped[Optional[int]]
    red_pick_3: Mapped[Optional[int]]
    red_ban_4: Mapped[Optional[int]]
    blue_ban_4: Mapped[Optional[int]]
    red_ban_5: Mapped[Optional[int]]
    blue_ban_5: Mapped[Optional[int]]
    red_pick_4: Mapped[Optional[int]]
    blue_pick_4: Mapped[Optional[int]]
    blue_pick_5: Mapped[Optional[int]]
    red_pick_5: Mapped[Optional[int]]

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
    __table_args__ = tuple(
        [
            *[
                ForeignKeyConstraint([pick], ["champion.id"], f"matchup_map_{pick}_fkey")
                for pick in ALL_PICKS
            ],
            *PicksBans.__table_args__,
        ]
    )

    blue_baron_pick: Mapped[Optional[int]]
    blue_jungle_pick: Mapped[Optional[int]]
    blue_mid_pick: Mapped[Optional[int]]
    blue_dragon_pick: Mapped[Optional[int]]
    blue_sup_pick: Mapped[Optional[int]]
    red_baron_pick: Mapped[Optional[int]]
    red_mid_pick: Mapped[Optional[int]]
    red_jungle_pick: Mapped[Optional[int]]
    red_dragon_pick: Mapped[Optional[int]]
    red_sup_pick: Mapped[Optional[int]]

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
    @declared_attr
    def __table_args__(cls):
        return tuple(
            ForeignKeyConstraint([player], ["player.id"], f"matchup_map_{player}_fkey")
            for player in ALL_PLAYERS
        )

    blue_baron_player: Mapped[Optional[int]]
    blue_jungle_player: Mapped[Optional[int]]
    blue_mid_player: Mapped[Optional[int]]
    blue_dragon_player: Mapped[Optional[int]]
    blue_sup_player: Mapped[Optional[int]]
    red_baron_player: Mapped[Optional[int]]
    red_mid_player: Mapped[Optional[int]]
    red_jungle_player: Mapped[Optional[int]]
    red_dragon_player: Mapped[Optional[int]]
    red_sup_player: Mapped[Optional[int]]

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
    blue_baron_kills: Mapped[Optional[int]] = mapped_column(default=0)
    blue_jungle_kills: Mapped[Optional[int]] = mapped_column(default=0)
    blue_mid_kills: Mapped[Optional[int]] = mapped_column(default=0)
    blue_dragon_kills: Mapped[Optional[int]] = mapped_column(default=0)
    blue_sup_kills: Mapped[Optional[int]] = mapped_column(default=0)
    red_baron_kills: Mapped[Optional[int]] = mapped_column(default=0)
    red_jungle_kills: Mapped[Optional[int]] = mapped_column(default=0)
    red_mid_kills: Mapped[Optional[int]] = mapped_column(default=0)
    red_dragon_kills: Mapped[Optional[int]] = mapped_column(default=0)
    red_sup_kills: Mapped[Optional[int]] = mapped_column(default=0)
    blue_baron_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    blue_jungle_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    blue_mid_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    blue_dragon_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    blue_sup_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    red_baron_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    red_jungle_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    red_mid_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    red_dragon_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    red_sup_deaths: Mapped[Optional[int]] = mapped_column(default=0)
    blue_baron_assists: Mapped[Optional[int]] = mapped_column(default=0)
    blue_jungle_assists: Mapped[Optional[int]] = mapped_column(default=0)
    blue_mid_assists: Mapped[Optional[int]] = mapped_column(default=0)
    blue_dragon_assists: Mapped[Optional[int]] = mapped_column(default=0)
    blue_sup_assists: Mapped[Optional[int]] = mapped_column(default=0)
    red_baron_assists: Mapped[Optional[int]] = mapped_column(default=0)
    red_jungle_assists: Mapped[Optional[int]] = mapped_column(default=0)
    red_mid_assists: Mapped[Optional[int]] = mapped_column(default=0)
    red_dragon_assists: Mapped[Optional[int]] = mapped_column(default=0)
    red_sup_assists: Mapped[Optional[int]] = mapped_column(default=0)

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
    blue_baron_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    blue_jungle_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    blue_mid_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    blue_dragon_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    blue_sup_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    red_baron_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    red_jungle_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    red_mid_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    red_dragon_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)
    red_sup_dmg_taken: Mapped[Optional[int]] = mapped_column(default=0)

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
    blue_baron_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    blue_jungle_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    blue_mid_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    blue_dragon_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    blue_sup_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    red_baron_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    red_jungle_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    red_mid_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    red_dragon_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)
    red_sup_dmg_dealt: Mapped[Optional[int]] = mapped_column(default=0)

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
    blue_baron_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    blue_jungle_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    blue_mid_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    blue_dragon_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    blue_sup_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    red_baron_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    red_jungle_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    red_mid_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    red_dragon_total_gold: Mapped[Optional[int]] = mapped_column(default=0)
    red_sup_total_gold: Mapped[Optional[int]] = mapped_column(default=0)

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
    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                ["team_first_blood"],
                ["team.id"],
                "matchup_map_team_first_blood_fkey",
            ),
            ForeignKeyConstraint(
                ["player_first_blood"],
                ["player.id"],
                "matchup_map_player_first_blood_fkey",
            ),
            ForeignKeyConstraint(
                ["player_first_death"],
                ["player.id"],
                "matchup_map_player_first_death_fkey",
            ),
        )

    team_first_blood: Mapped[Optional[int]]
    player_first_blood: Mapped[Optional[int]]
    player_first_death: Mapped[Optional[int]]
    place_first_blood: Mapped[Optional[str]]

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
    @declared_attr
    def __table_args__(cls):
        return [
            ForeignKeyConstraint(
                ["team_first_tower"],
                ["team.id"],
                "matchup_map_team_first_tower_fkey",
            ),
        ]

    team_first_tower: Mapped[Optional[int]]
    first_tower_route: Mapped[Optional[Role]]
    first_tower_herald: Mapped[Optional[bool]] = mapped_column(default=False)

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

    @declared_attr
    def __table_args__(cls):
        return [
            ForeignKeyConstraint(
                ["team_first_herald"],
                ["team.id"],
                "matchup_map_team_first_herald_fkey",
            ),
        ]

    team_first_herald: Mapped[Optional[int]]
    first_herald_teamfight: Mapped[Optional[bool]] = mapped_column(default=False)
    first_herald_stealed: Mapped[Optional[bool]] = mapped_column(default=False)
    first_herald_route: Mapped[Optional[str]]

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

    @declared_attr
    def __table_args__(cls):
        return [
            ForeignKeyConstraint(
                ["team_second_herald"],
                ["team.id"],
                "matchup_map_team_second_herald_fkey",
            ),
        ]

    team_second_herald: Mapped[Optional[int]]
    second_herald_teamfight: Mapped[Optional[bool]] = mapped_column(default=False)
    second_herald_stealed: Mapped[Optional[bool]] = mapped_column(default=False)
    second_herald_route: Mapped[Optional[str]]

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstHerald()
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

    @declared_attr
    def __table_args__(cls):
        return [
            ForeignKeyConstraint(
                ["team_first_drake"],
                ["team.id"],
                "matchup_map_team_first_drake_fkey",
            ),
        ]

    team_first_drake: Mapped[Optional[int]]
    first_drake_teamfight: Mapped[Optional[bool]] = mapped_column(default=False)
    first_drake_stealed: Mapped[Optional[bool]] = mapped_column(default=False)
    first_drake_type: Mapped[Optional[str]]

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

    @declared_attr
    def __table_args__(cls):
        return [
            ForeignKeyConstraint(
                ["team_second_drake"],
                ["team.id"],
                "matchup_map_team_second_drake_fkey",
            ),
        ]

    team_second_drake: Mapped[Optional[int]]
    second_drake_teamfight: Mapped[Optional[bool]] = mapped_column(default=False)
    second_drake_stealed: Mapped[Optional[bool]] = mapped_column(default=False)
    second_drake_type: Mapped[Optional[str]]

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstDrake()
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

    @declared_attr
    def __table_args__(cls):
        return [
            ForeignKeyConstraint(
                ["team_third_drake"],
                ["team.id"],
                "matchup_map_team_third_drake_fkey",
            ),
        ]

    team_third_drake: Mapped[Optional[int]]
    third_drake_teamfight: Mapped[Optional[bool]] = mapped_column(default=False)
    third_drake_stealed: Mapped[Optional[bool]] = mapped_column(default=False)
    third_drake_type: Mapped[Optional[str]]

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FirstDrake()
        obj.team_third_drake = kwargs.get("team_third_drake")
        obj.third_drake_teamfight = kwargs.get("third_drake_teamfight")
        obj.third_drake_stealed = kwargs.get("third_drake_stealed")
        obj.third_drake_type = kwargs.get("third_drake_type")
