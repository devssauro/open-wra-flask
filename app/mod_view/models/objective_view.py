from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from db_config import db


class ObjectiveView(db.Model, SerializerMixin):
    __tablename__ = "objective_view"

    uuid: Mapped[Optional[str]] = mapped_column(type_=UUID, primary_key=True)
    matchup_id: Mapped[Optional[int]]
    map_id: Mapped[Optional[int]]
    map_number: Mapped[Optional[int]]
    patch: Mapped[Optional[str]]
    side: Mapped[Optional[str]]
    tournament_id: Mapped[Optional[int]]
    winner: Mapped[Optional[bool]]
    length: Mapped[Optional[str]]
    length_sec: Mapped[Optional[int]]
    team_id: Mapped[Optional[int]]
    team_giver_id: Mapped[Optional[int]]
    objective_type: Mapped[Optional[str]]
    objective_name: Mapped[Optional[str]]
    objective_order: Mapped[Optional[int]]
    with_teamfight: Mapped[Optional[bool]]
    is_stealed: Mapped[Optional[bool]]
    place: Mapped[Optional[str]]
    with_herald: Mapped[Optional[bool]]
    killer: Mapped[Optional[int]]
    role_killer: Mapped[Optional[str]]
    champion_killer: Mapped[Optional[int]]
    victim: Mapped[Optional[int]]
    role_victim: Mapped[Optional[str]]
    champion_victim: Mapped[Optional[int]]
