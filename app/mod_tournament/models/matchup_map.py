from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
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


class Objectives(
    FirstBlood,
    FirstTower,
    FirstHerald,
    SecondHerald,
    FirstDrake,
    SecondDrake,
    ThirdDrake,
):
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
    blue_turrets_destroyed = Column(Integer, default=0)
    red_turrets_destroyed = Column(Integer, default=0)

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
