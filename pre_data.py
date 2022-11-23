from datetime import datetime
from uuid import uuid4

from flask_security import hash_password

from app import create_app
from app.mod_auth.models import Role, User
from db_config import db
from security_config import user_datastore

create_app().app_context().push()


def create_roles():
    print("CREATING ROLES")
    admin = user_datastore.find_role("admin")
    if not admin:
        admin = Role()
        admin.name = "admin"
        admin.description = "Administrador"
        admin.permissions = ",".join(
            {
                "admin-read",
                "admin-write",
                "admin-update",
                "admin-remove",
                "op-read",
                "analyst-read",
            }
        )
        db.session.add(admin)
    op = user_datastore.find_role("operational")
    if not op:
        op = Role()
        op.name = "operational"
        op.description = "Operacional"
        op.permissions = ",".join({"op-read", "op-remove", "op-write"})
        db.session.add(op)
    analyst = user_datastore.find_role("analyst")
    if not analyst:
        analyst = Role()
        analyst.name = "analyst"
        analyst.description = "Analista"
        analyst.permissions = ",".join({"analyst-read"})
        db.session.add(analyst)
    db.session.commit()
    print("ROLES CREATED")
    return admin, op, analyst


def create_admin_users(admin, op, analyst):
    print("CREATING USERS")
    adm = User()
    if not user_datastore.find_user(username="devssauro"):
        adm.email = "cunha.ladm@outlook.com"
        adm.password = hash_password("123546")
        adm.username = "devssauro"
        adm.fs_uniquifier = uuid4().hex
        adm.confirmed_at = datetime.now()
        db.session.add(adm)
    else:
        adm = user_datastore.find_user(username="devssauro")

    yumi = User()
    if not user_datastore.find_user(username="yumilina"):
        yumi.email = "yumilia@gmail.com"
        yumi.password = hash_password("123456")
        yumi.username = "yumilina"
        yumi.fs_uniquifier = uuid4().hex
        yumi.confirmed_at = datetime.now()
        db.session.add(yumi)
    else:
        yumi = user_datastore.find_user(username="yumilina")

    print("USERS CREATED")

    print("ADDING ROLES TO USERS")
    db.session.commit()
    user_datastore.add_role_to_user(adm, admin)
    user_datastore.add_role_to_user(adm, op)
    user_datastore.add_role_to_user(adm, analyst)
    user_datastore.add_role_to_user(yumi, analyst)
    user_datastore.commit()
    print("ROLES TO USERS ADDED")


create_admin_users(*create_roles())
