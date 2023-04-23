from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from app.mod_view.models.abstracts import ObjectiveFields
from db_config import db


class PicksBansPrioView(db.Model, ObjectiveFields, SerializerMixin):
    __tablename__ = "picks_bans_prio_view"

    uuid: Mapped[Optional[str]] = mapped_column(type_=UUID, primary_key=True)
    matchup_id: Mapped[Optional[int]]
    map_id: Mapped[Optional[int]]
    map_number: Mapped[Optional[int]]
    patch: Mapped[Optional[str]]
    side: Mapped[Optional[str]]
    length: Mapped[Optional[str]]
    length_sec: Mapped[Optional[int]]
    tournament_id: Mapped[Optional[int]]
    team_id: Mapped[Optional[int]]
    winner: Mapped[Optional[bool]]
    ban_id: Mapped[Optional[int]]
    pick_id: Mapped[Optional[str]]
    position: Mapped[Optional[int]]
    pick_rotation: Mapped[Optional[int]]
    ban_rotation: Mapped[Optional[int]]
    role: Mapped[Optional[str]]
    is_blind: Mapped[Optional[bool]]
    player: Mapped[Optional[int]]
    kills: Mapped[Optional[int]]
    deaths: Mapped[Optional[int]]
    assists: Mapped[Optional[int]]
    dmg_taken: Mapped[Optional[int]]
    dmg_dealt: Mapped[Optional[int]]
    total_gold: Mapped[Optional[int]]
    is_player_first_blood: Mapped[Optional[bool]]
    is_player_first_death: Mapped[Optional[bool]]
