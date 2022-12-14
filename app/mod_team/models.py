from enum import IntEnum, unique

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from db_config import Base


@unique
class Role(IntEnum):
    baron = 1
    jungle = 2
    mid = 3
    dragon = 4
    sup = 5


class Team(Base, SerializerMixin):
    __tablename__ = "team"
    serialize_only = ("id", "name", "tag", "flag")

    def __init__(self, name, tag, flag, phase=None):
        self.name = name
        self.tag = tag
        self.flag = flag
        self.phase = phase

    name: str | Column = Column(String)
    tag: str | Column = Column(String)
    flag: str | Column = Column(String)
    phase: str | Column = Column(String)

    lineups: list = relationship("TournamentTeam", back_populates="team")
    matchups_1: list = relationship(
        "Matchup", foreign_keys="Matchup.team1_id", back_populates="team1"
    )
    matchups_2: list = relationship(
        "Matchup", foreign_keys="Matchup.team2_id", back_populates="team2"
    )

    @property
    def matchups(self):
        return [*self.matchups_1, *self.matchups_2]


class Player(Base, SerializerMixin):
    __tablename__ = "player"
    serialize_only = ("id", "nickname", "flag")

    def __int__(self, nickname, team_id, flag, role):
        self.nickname = nickname
        self.team_id = team_id
        self.flag = flag
        self.role = role

    nickname: str | Column = Column(String)
    team_id: int | Column = Column(Integer, ForeignKey("team.id"))
    # team = relationship("Team", back_populates="players")
    flag: str | Column = Column(String)
    role: Role | Column = Column(Enum(Role))
