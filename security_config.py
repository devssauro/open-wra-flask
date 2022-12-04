from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect

from app.mod_auth.models import Role, User
from db_config import db

csrf = CSRFProtect()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
