from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin

from db_config import Base


class Champion(Base, SerializerMixin):
    """Class to represent a champion from a game

    Attributes:
        name (str): name of the champion
    """

    __tablename__ = "champion"
    serialize_only = ("id", "name", "riot_id", "avatar")

    def __int__(self, name, avatar, riot_id):
        self.name = name
        self.avatar = avatar
        self.riot_id = riot_id

    name: str | Column = Column(String)
    avatar: str | Column = Column(String)
    riot_id: str | Column = Column(String)
