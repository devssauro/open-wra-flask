from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.mod_tournament.models.abstracts import (
    KDA,
    DamageDealt,
    DamageTaken,
    Draft,
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


class MatchupMap(
    Base,
    Draft,
    FirstDrake,
    FirstHerald,
    FirstTower,
    Players,
    DamageTaken,
    DamageDealt,
    SecondDrake,
    SecondHerald,
    ThirdDrake,
    TotalGold,
    KDA,
    SerializerMixin,
):
    """Class to represent a map in a matchup"""

    __tablename__ = "matchup_map"

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
    def from_payload(**kwargs) -> "MatchupMap":
        map = MatchupMap()

        map.matchup_id = kwargs.get("matchup_id")
        map.tournament_id = kwargs.get("tournament_id")
        map.vod_link = kwargs.get("vod_link")
        map.patch = kwargs.get("patch")
        map.blue_side = kwargs.get("blue_side")
        map.red_side = kwargs.get("red_side")
        map.length = kwargs.get("length")
        map.winner = kwargs.get("winner")
        map.winner_side = kwargs.get("winner_side")

        return map
