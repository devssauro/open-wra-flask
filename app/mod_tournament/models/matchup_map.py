from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.mod_tournament.models.abstracts import (
    KDA,
    DamageDealt,
    DamageTaken,
    FirstDrake,
    FirstHerald,
    FirstTower,
    PicksBans,
    Players,
    SecondDrake,
    SecondHerald,
    ThirdDrake,
    TotalGold,
)
from db_config import Base


class MatchupMap(
    Base,
    FirstDrake,
    FirstHerald,
    FirstTower,
    PicksBans,
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
    blue_turrets_destroyed = Column(Integer, default=0)
    red_turrets_destroyed = Column(Integer, default=0)
