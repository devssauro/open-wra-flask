from enum import IntEnum, unique
from typing import List, Optional

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    name: Mapped[Optional[str]]
    tag: Mapped[Optional[str]]
    flag: Mapped[Optional[str]]
    phase: Mapped[Optional[str]]

    lineups: Mapped[List["TournamentTeam"]] = relationship(backref="team")  # noqa: F821

    @property
    def matchups(self) -> list:  # noqa: F821
        return [*self.matchups_1, *self.matchups_2]


class Player(Base, SerializerMixin):
    __tablename__ = "player"
    serialize_only = ("id", "nickname", "flag")

    def __int__(self, nickname, team_id, flag, role):
        super(Base).__init__()
        super(SerializerMixin).__init__()
        self.nickname = nickname
        self.team_id = team_id
        self.flag = flag
        self.role = role

    nickname: Mapped[Optional[str]]
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    flag: Mapped[Optional[str]] = Column(String)
    role: Mapped[Optional[Role]] = Column(type_=Enum(Role))
    matchup_mvps: Mapped[List["Matchup"]] = relationship(backref="mvp")  # noqa: F821
