from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.mod_tournament.models.abstracts import (  # Players,
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
    def from_payload(**kwargs):
        _map = MatchupMap()
        _map.matchup_id = (kwargs.get("matchup_id"),)
        _map.tournament_id = (kwargs.get("tournament_id"),)
        _map.vod_link = (kwargs.get("vod_link"),)
        _map.map_number = (kwargs.get("map_number"),)
        _map.patch = (kwargs.get("patch"),)
        _map.blue_side = (kwargs.get("blue_side"),)
        _map.red_side = (kwargs.get("red_side"),)
        _map.length = (kwargs.get("length"),)
        _map.winner = (kwargs.get("winner"),)
        _map.winner_side = (kwargs.get("winner_side"),)
        _map.blue_turrets_destroyed = (kwargs.get("blue_turrets_destroyed"),)
        _map.red_turrets_destroyed = (kwargs.get("red_turrets_destroyed"),)

        super(Draft, _map).from_payload(_map, **kwargs)

        return _map
