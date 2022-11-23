from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from db_config import db


class ObjectiveView(db.Model, SerializerMixin):
    __tablename__ = "objective_view"

    uuid = Column(UUID, primary_key=True)
    matchup_id = Column(Integer)
    map_id = Column(Integer)
    map_number = Column(Integer)
    patch = Column(String)
    side = Column(String)
    tournament_id = Column(Integer)
    winner = Column(Boolean)
    length = Column(String)
    length_sec = Column(Integer)
    team_id = Column(Integer)
    team_giver_id = Column(Integer)
    objective_type = Column(String)
    objective_name = Column(String)
    objective_order = Column(Integer)
    with_teamfight = Column(Boolean)
    is_stealed = Column(Boolean)
    place = Column(String)
    with_herald = Column(Boolean)
    killer = Column(Integer)
    role_killer = Column(String)
    champion_killer = Column(Integer)
    victim = Column(Integer)
    role_victim = Column(String)
    champion_victim = Column(Integer)
