from flask_security import ConfirmRegisterForm, Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired

from app.mod_auth.models import Role, User
from db_config import db

csrf = CSRFProtect()


class ExtendedRegisterForm(ConfirmRegisterForm):
    extra = StringField("extra", [DataRequired()])


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(confirm_register_form=ExtendedRegisterForm)
