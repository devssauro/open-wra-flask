from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    Mapped,
    declarative_mixin,
    declared_attr,
    mapped_column,
    relationship,
)
from sqlalchemy_serializer import SerializerMixin

from app.mod_tournament.models.abstracts import (
    KDA,
    DamageDealt,
    DamageTaken,
    Draft,
    FirstBlood,
    FirstDrake,
    FirstHerald,
    FirstTower,
    Players,
    SecondDrake,
    SecondHerald,
    ThirdDrake,
    TotalGold,
)
from db_config import Base


class FinalStats(
    DamageTaken,
    DamageDealt,
    KDA,
    TotalGold,
):
    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = FinalStats()

        DamageTaken.from_payload(obj, **kwargs)
        DamageDealt.from_payload(obj, **kwargs)
        KDA.from_payload(obj, **kwargs)
        TotalGold.from_payload(obj, **kwargs)

        return obj


@declarative_mixin
class Objectives(
    FirstBlood,
    FirstTower,
    FirstHerald,
    SecondHerald,
    FirstDrake,
    SecondDrake,
    ThirdDrake,
):
    @declared_attr
    def __table_args__(cls):
        return tuple(
            [
                *FirstBlood.__table_args__,
                *FirstTower.__table_args__,
                *FirstHerald.__table_args__,
                *SecondHerald.__table_args__,
                *FirstDrake.__table_args__,
                *SecondDrake.__table_args__,
                *ThirdDrake.__table_args__,
            ]
        )

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = Objectives()

        FirstBlood.from_payload(obj, **kwargs)
        FirstTower.from_payload(obj, **kwargs)
        FirstHerald.from_payload(obj, **kwargs)
        SecondHerald.from_payload(obj, **kwargs)
        FirstDrake.from_payload(obj, **kwargs)
        SecondDrake.from_payload(obj, **kwargs)
        ThirdDrake.from_payload(obj, **kwargs)

        return obj


class MatchupMap(
    Base,
    Draft,
    Players,
    SerializerMixin,
    FinalStats,
    Objectives,
):
    """Class to represent a map in a matchup"""

    __tablename__ = "matchup_map"

    @declared_attr
    def __table_args__(cls):
        return tuple(
            [
                *Draft.__table_args__,
                *Players.__table_args__,
                *Objectives.__table_args__,
            ],
        )

    def __init__(
        self,
        matchup_id=None,
        tournament_id=None,
        vod_link=None,
        map_number=None,
        patch=None,
        blue_side=None,
        red_side=None,
        length=None,
        winner=None,
        winner_side=None,
        blue_turrets_destroyed=None,
        red_turrets_destroyed=None,
    ):
        self.matchup_id = matchup_id
        self.tournament_id = tournament_id
        self.vod_link = vod_link
        self.map_number = map_number
        self.patch = patch
        self.blue_side = blue_side
        self.red_side = red_side
        self.length = length
        self.winner = winner
        self.winner_side = winner_side
        self.blue_turrets_destroyed = blue_turrets_destroyed
        self.red_turrets_destroyed = red_turrets_destroyed
        super().__init__()

    matchup_id: Mapped[Optional[int]] = mapped_column(ForeignKey("matchup.id"))
    matchup: Mapped["Matchup"] = relationship(back_populates="maps")  # noqa: F821
    tournament_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tournament.id"))
    vod_link: Mapped[Optional[str]]
    map_number: Mapped[Optional[int]]
    patch: Mapped[Optional[str]]
    blue_side: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    red_side: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    length: Mapped[Optional[str]] = mapped_column(String)
    winner: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    winner_side: Mapped[Optional[str]] = mapped_column(String)
    blue_turrets_destroyed: Mapped[Optional[int]] = mapped_column(default=0)
    red_turrets_destroyed: Mapped[Optional[int]] = mapped_column(default=0)

    @staticmethod
    def from_payload(obj=None, **kwargs):
        if obj is None:
            obj = MatchupMap()

        Draft.from_payload(obj, **kwargs)
        Players.from_payload(obj, **kwargs)
        Objectives.from_payload(obj, **kwargs)
        FinalStats.from_payload(obj, **kwargs)

        obj.matchup_id = (kwargs.get("matchup_id"),)
        obj.tournament_id = (kwargs.get("tournament_id"),)
        obj.vod_link = (kwargs.get("vod_link"),)
        obj.map_number = (kwargs.get("map_number"),)
        obj.patch = (kwargs.get("patch"),)
        obj.blue_side = (kwargs.get("blue_side"),)
        obj.red_side = (kwargs.get("red_side"),)
        obj.length = (kwargs.get("length"),)
        obj.winner = (kwargs.get("winner"),)
        obj.winner_side = (kwargs.get("winner_side"),)
        obj.blue_turrets_destroyed = (kwargs.get("blue_turrets_destroyed"),)
        obj.red_turrets_destroyed = (kwargs.get("red_turrets_destroyed"),)

        return obj
