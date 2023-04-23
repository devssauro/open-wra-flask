from datetime import datetime
from typing import List, Optional

from flask_security import RoleMixin, UserMixin
from sqlalchemy import TEXT, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_config import Base, db

# class RolesUsers(Base):
#     __tablename__ = "auth_role_user"
#     # extend_existing = True
#     user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("auth_user.id"))
#     role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("auth_role.id"))
RolesUsers = Table(
    "association_table",
    db.metadata,
    Column("user_id", ForeignKey("auth_user.id")),
    Column("role_id", ForeignKey("auth_role.id")),
)


class Role(Base, RoleMixin):
    __tablename__ = "auth_role"
    name: Mapped[Optional[str]] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    permissions: Mapped[Optional[str]] = mapped_column(type_=TEXT)


class User(Base, UserMixin):
    __tablename__ = "auth_user"
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    username: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    password: Mapped[Optional[str]] = mapped_column(nullable=False)
    last_login_at: Mapped[Optional[datetime]]
    current_login_at: Mapped[Optional[datetime]]
    last_login_ip: Mapped[Optional[str]]
    current_login_ip: Mapped[Optional[str]]
    login_count: Mapped[Optional[int]]
    fs_uniquifier: Mapped[Optional[str]] = mapped_column(unique=True, nullable=False)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column()
    roles: Mapped[List[Role]] = relationship(secondary=RolesUsers)

    def get_security_payload(self):
        rv = super().get_security_payload()
        rv["name"] = self.extra.get("name", "")
        rv["username"] = self.username
        rv["roles"] = [role.name for role in self.roles]
        return rv
