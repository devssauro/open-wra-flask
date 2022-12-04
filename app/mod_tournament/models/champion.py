from sqlalchemy import Column, String
from sqlalchemy_serializer import SerializerMixin

from db_config import Base


class Champion(Base, SerializerMixin):
    """Class to represent a champion from a game

    Attributes:
        name (str): name of the champion
    """

    __tablename__ = "champion"
    serialize_only = ("id", "name")

    def __int__(self, name):
        self.name = name

    name: str | Column = Column(String)
