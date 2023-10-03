# Open WRA Python
About the project: the system was made to create a datavis tool to analize the metagaming
on [Icons Global Championship 2022](https://liquipedia.net/wildrift/Icons_Global_Championship/2022) to help the
3 brazilian teams to perform and reach the best position they can on the tournament.

The initial deadline was 3 weeks, it started right after the [Wild Tour Brazil 2022 Season 1
](https://liquipedia.net/wildrift/Wild_Tour/2022/Season_1) and the first version was made using Flask 2 recently launched, VueJS 2 and vuetify on frontend, PostgreSQL and SQLAlchemy 1.4.

Because Riot Games decided to end the official tournaments on western side of the globe to focus on Asia (you can see more about it [here](https://esports-news.co.uk/2022/11/22/riot-ditches-wild-rift-esports-west/#:~:text=Wild%20Rift%20esports%20has%20effectively,Wild%20Rift%20esports%20leagues%20anymore.)), where the market is big, my decision was to turn the whole software open source to help the community and show a bit of my work.

Now it's my sandbox to test some implementations like SQLAlchemy 2, test skills like the automated tests I wrote for it and other skills.

I made 2 frontends for this project, one written in [VueJS 2](https://github.com/devssauro/vue-wra) and another using [Vue 3, but it's incomplete](https://github.com/devssauro/open-wra-vue3).

I also made an implementation using [Streamlit](https://streamlit.io/) that works consuming an endpoint that brings some CSV files from the platform, [you can see the code here](https://github.com/devssauro/wildrift-analytics)

As you can see, it's a sandbox, but feel free to evaluate my job.

## Installation instructions
By running `docker compose up`, the whole project will be launched for use,
After that run `flask db upgrade` to instantiate the database.

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
