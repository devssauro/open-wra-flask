from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from db_config import Base


class TournamentLineup(Base, SerializerMixin):
    """Class to represent all players froma team in a tournament

    Attributes:
        tournament_team_id (int): The tournament's id
        player_id (int): The player_id
    """

    __tablename__ = "tournament_lineup"

    def __init__(self, tournament_team_id, player_id):
        self.tournament_team_id = tournament_team_id
        self.player_id = player_id

    tournament_team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tournament_team.id"))
    player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player.id"))
