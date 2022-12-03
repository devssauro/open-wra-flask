from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from db_config import Base


class Matchup(Base, SerializerMixin):
    """Class to a matchup in a tournament

    A matchup is the Best of 3/5/7.

    Attributes:
        phase (str): The phase of the tournament where that matchup occurred
        datetime (datetime): The date and the time in hours when the matchup happened
        mvp_id (str): The player's id MVP for the matchup
        tournament_id (str): The tournament's id
        team1_id (int): The first team's id
        team2_id (int): The second team's id
        vod_link (str): The vod link to the matches
    """

    __tablename__ = "matchup"
    serialize_only = (
        "id",
        "datetime",
        "mvp_id",
        "tournament_id",
        "team1_id",
        "team2_id",
        "vod_link",
    )

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
