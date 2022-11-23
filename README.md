# Open WRA Python

## Installation instructions

### Database

Install a PostgreSQL database locally on your system
and create a database to manage data

### Environment variables

Use the `.env.example` file to set up all the environment variables
for your application

#### Variables

- DEBUG: to setup your environment in a debug mode
- FLASL_DEBUG: to enable the debugging on shell
- FLASK_RUN_PORT: the port number the application runs
- SQLALCHEMY_DATABASE: the database address express like:
`postgresql://user:password@address:port/db_wr` commonly setted with
the default values
- SECRET_KEY: the secret key for authentication method
- SECURITY_PASSWORD_SALT: the salt used to Flask-Security library
gerenate a new one running `secrets.SystemRandom().getrandbits(128)`
on Python Shell
- SECURITY_PASSWORD_HASH: the hashing method used to hash passwords.
The default value is `pbkdf2_sha512`
- MAIL_SERVER: the server to enable mailing integration on system
- MAIL_PORT: the port to the mail server.
- MAIL_USE_SSL: the indicator to use SSL.
- MAIL_USE_TLS: the indicator to use TLS.
- MAIL_USERNAME: the mail username to be integrated with the platform.
- MAIL_PASSWORD: the mail password to be integrated with the platform.
- CORS_ORIGINS: all the hosts allowed to connect with the backend
- FRONT_URL: the address to the front-end URL
- FIREBASE_STORAGE: the firebase storage pointed to application

### Virtual Environment

1. Create a new virtual environment using the command `python3 -m venv venv`.
2. Access the virtual environment using the command `source venv/bin/activate`.
3. Install all the required packages with `pip install -r requirements.txt`.

### Set up the database

With the virtual environment setted up and the database created
and setted on virtual envionments, run the command `flask db upgrade`
to create all the tables on the database.

### Running the application

To run the application you can simply run `flask run` on shell
or execute the `run_debug.py` on your PyCharm
