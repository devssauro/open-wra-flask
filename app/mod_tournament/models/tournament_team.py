from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
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
    serialize_only = ("id", "team_id", "entry_phase")

    def __init__(self, tournament_id, team_id, entry_phase):
        self.tournament_id = tournament_id
        self.team_id = team_id
        self.entry_phase = entry_phase

    tournament_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tournament.id"))
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    entry_phase: Mapped[Optional[str]] = mapped_column(String)

    tournament: Mapped[Optional[List["Tournament"]]] = relationship(backref="teams")  # noqa: F821
    players: Mapped[Optional[list["Player"]]] = relationship(
        secondary="tournament_lineup", backref=backref("lineups", lazy="dynamic")
    )
