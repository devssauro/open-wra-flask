from decouple import config

# SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
DEBUG = config("DEBUG", cast=bool)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = config("JWT_SECRET_KEY")
REDIRECT_ALLOW_SUBDOMAINS = True
SESSION_COOKIE_DOMAIN = False
# SERVER_NAME = config('FRONT_URL')

# Flask-Security stuff
SECRET_KEY = config("SECRET_KEY")
SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT")
SECURITY_PASSWORD_HASH = config("SECURITY_PASSWORD_HASH")
SECURITY_FLASH_MESSAGES = False
SECURITY_URL_PREFIX = "/api"

SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
# SECURITY_UNIFIED_SIGNIN = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
SECURITY_AUTO_LOGIN_AFTER_CONFIRM = False
SECURITY_POST_CONFIRM_VIEW = "/confirmed"
SECURITY_CONFIRM_ERROR_VIEW = "/confirm-error"
SECURITY_RESET_VIEW = "/reset-password"
SECURITY_RESET_ERROR_VIEW = "/reset-password"
SECURITY_REDIRECT_BEHAVIOR = "spa"
SECURITY_POST_LOGOUT_VIEW = ""

SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

SECURITY_CSRF_COOKIE_NAME = None
SECURITY_CSRF_HEADER = "X-CSRF-Token"
WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_TIME_LIMIT = None
WTF_CSRF_HEADERS = ["X-CSRF-Token", "X-XSRF-Token", "XCSRF-Token"]

SECURITY_REDIRECT_HOST = config("FRONT_URL")
SECURITY_REDIRECT_ALLOW_SUBDOMAINS = True

# SECURITY_USERNAME_ENABLE = True
# SECURITY_USERNAME_REQUIRED = True
