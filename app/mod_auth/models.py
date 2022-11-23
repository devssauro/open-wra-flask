from flask_security import RoleMixin, UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UnicodeText
from sqlalchemy.orm import backref, relationship

from db_config import Base


class RolesUsers(Base):
    __tablename__ = "auth_role_user"
    extend_existing = True
    user_id = Column(Integer(), ForeignKey("auth_user.id"))
    role_id = Column(Integer(), ForeignKey("auth_role.id"))


class Role(Base, RoleMixin):
    __tablename__ = "auth_role"
    name = Column(String(), unique=True)
    description = Column(String())
    permissions = Column(UnicodeText)


class User(Base, UserMixin):
    __tablename__ = "auth_user"
    email = Column(String(255), unique=True)
    username = Column(String(14), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship(
        "Role", secondary="auth_role_user", backref=backref("users", lazy="dynamic")
    )

    def get_security_payload(self):
        rv = super().get_security_payload()
        rv["name"] = self.extra.get("name", "")
        rv["username"] = self.username
        rv["roles"] = [role.name for role in self.roles]
        return rv
