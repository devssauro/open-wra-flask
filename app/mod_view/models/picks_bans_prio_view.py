from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from app.mod_view.models.abstracts import ObjectiveFields
from db_config import db


class PicksBansPrioView(db.Model, ObjectiveFields, SerializerMixin):
    __tablename__ = "picks_bans_prio_view"

    uuid = Column(UUID, primary_key=True)
    matchup_id = Column(Integer)
    map_id = Column(Integer)
    map_number = Column(Integer)
    patch = Column(String)
    side = Column(String)
    length = Column(String)
    length_sec = Column(Integer)
    tournament_id = Column(Integer)
    team_id = Column(Integer)
    winner = Column(Boolean)
    ban_id = Column(Integer)
    pick_id = Column(String)
    position = Column(Integer)
    pick_rotation = Column(Integer)
    ban_rotation = Column(Integer)
    role = Column(String)
    is_blind = Column(Boolean)
    player = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    dmg_taken = Column(Integer)
    dmg_dealt = Column(Integer)
    total_gold = Column(Integer)
    is_player_first_blood = Column(Boolean)
    is_player_first_death = Column(Boolean)
