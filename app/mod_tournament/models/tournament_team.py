from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy_serializer import SerializerMixin

from app.mod_team.models import Player
from db_config import Base


class TournamentTeam(Base, SerializerMixin):
    """Class to represent all teams of a tournament

    Attributes:
        tournament_id (int): The tournament's id
        team_id (int): The team's id
        entry_phase (str): The entry phase that team started on a tournament
        players (list): The team's players
    """

    __tablename__ = "tournament_team"

    def __init__(self, tournament_id, team_id, entry_phase):
        self.tournament_id = tournament_id
        self.team_id = team_id
        self.entry_phase = entry_phase

    tournament_id: int | Column = Column(Integer, ForeignKey("tournament.id"))
    team_id: int | Column = Column(Integer, ForeignKey("team.id"))
    entry_phase: str | Column = Column(String)

    tournament: list = relationship("Tournament", back_populates="teams")
    team = relationship("Team", back_populates="lineups")
    players: list[Player] = relationship(
        "Player", secondary="tournament_lineup", backref=backref("lineups", lazy="dynamic")
    )
