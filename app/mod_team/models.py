from enum import IntEnum, unique

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
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

    def __init__(self, name, tag, flag, phase=None):
        self.name = name
        self.tag = tag
        self.flag = flag
        self.phase = phase

    name = Column(String)
    tag = Column(String)
    flag = Column(String)
    phase = Column(String)


class Player(Base, SerializerMixin):
    __tablename__ = "player"

    def __int__(self, nickname, team_id, flag, role):
        self.nickname = nickname
        self.team_id = team_id
        self.flag = flag
        self.role = role

    nickname = Column(String)
    team_id = Column(Integer, ForeignKey("team.id"))
    # team = relationship('Team', back_populates='players')
    flag = Column(String)
    role = Column(Enum(Role))
