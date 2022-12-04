from datetime import datetime

from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from db_config import Base


class Tournament(Base, SerializerMixin):
    """Class to represent all tournament

    Attributes:
        name (str): The tournament's name
        tag (str): The tournament's tag
        region (str): The tournament's region
        start_date (datetime): The tournament's start date
        end_date (datetime): The tournament's end date
        split (int): The tournament's split
        phases (int): The tournament's phases
        female_only (bool): The indicator if the tournament is female only
    """

    __tablename__ = "tournament"
    serialize_only = (
        "id",
        "name",
        "tag",
        "region",
        "start_date",
        "end_date",
        "split",
        "female_only",
        "teams",
    )

    def __init__(
        self,
        name,
        tag,
        region,
        start_date,
        end_date,
        split,
        phases: list | str,
        female_only: bool = False,
    ):
        self.name = name
        self.tag = tag
        self.region = region
        self.start_date = start_date
        self.end_date = end_date
        self.split = split
        if isinstance(phases, str):
            phases = phases.split(",")
        self.phases = phases
        self.female_only = female_only

    name: str | Column = Column(String)
    tag: str | Column = Column(String)
    region: str | Column = Column(String)
    start_date: datetime | Column = Column(DateTime)
    end_date: datetime | Column = Column(DateTime)
    split: int | Column = Column(Integer)
    phases: list[str] = Column(ARRAY(String))
    female_only: bool | Column = Column(Boolean, default=False)

    teams: list = relationship("TournamentTeam", back_populates="tournament")
