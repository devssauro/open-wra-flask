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
        name=None,
        tag=None,
        region=None,
        start_date=None,
        end_date=None,
        split=None,
        phases: list | str = [],
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
    phases: list[str] | str = Column(ARRAY(String))
    female_only: bool | Column = Column(Boolean, default=False)

    teams: list = relationship("TournamentTeam", back_populates="tournament")

    @staticmethod
    def from_payload(obj, **kwargs):
        if obj is None:
            obj = Tournament()

        obj.name = kwargs.get("name", None)
        obj.tag = kwargs.get("tag", None)
        obj.region = kwargs.get("region", None)
        obj.start_date = kwargs.get("start_date", None)
        obj.end_date = kwargs.get("end_date", None)
        obj.split = kwargs.get("split", None)
        obj.female_only = kwargs.get("female_only", None)
        obj._set_phases(kwargs.get("phases", None))

        return obj

    def _set_phases(self, phases: list | str | None = None):
        """Function to set phases of a tournament"""
        if isinstance(phases, str):
            self.phases = phases.split(",")
        if isinstance(phases, (list, tuple)) and len(phases) > 0:
            if isinstance(phases[0], str):
                self.phases = phases
            if isinstance(phases[0], dict):
                self.phases = [phase["name"] for phase in phases]
                if isinstance(self.extra, dict):
                    self.extra["phases"] = phases
                else:
                    self.extra = {"phases": phases}
