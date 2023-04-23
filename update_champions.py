import requests
from decouple import config

from app import create_app
from app.db_handler import DBHandler
from app.mod_tournament.models import Champion

DDRAGON_ENDPOINT = config("DDRAGON_ENDPOINT")
DDRAGON_LATEST_PATCH = config("DDRAGON_LATEST_PATCH")
DDRAGON_CHAMPION_DATA = config("DDRAGON_CHAMPION_DATA")
DDRAGON_CHAMPION_IMAGE = config("DDRAGON_CHAMPION_IMAGE")
BASE_ROUTE = f"{DDRAGON_ENDPOINT}{DDRAGON_LATEST_PATCH}"
CHAMPION_URL = f"{BASE_ROUTE}{DDRAGON_CHAMPION_DATA}"

create_app().app_context().push()
champions = DBHandler.get_champions()
champions_object = {champion.name: champion for champion in champions}

response = requests.get(CHAMPION_URL).json()["data"]
champions_data = {response[champion]["name"]: response[champion] for champion in response}

for champion in champions_data:
    champion_object: Champion | None = champions_object.get(champion)
    avatar_url = f"{BASE_ROUTE}{DDRAGON_CHAMPION_IMAGE}{champions_data[champion]['image']['full']}"
    if champion_object is not None:
        champion_object.avatar = avatar_url
        champion_object.riot_id = champions_data[champion]["key"]
    else:
        champion_object = Champion(
            name=champion,
            avatar=avatar_url,
            riot_id=champions_data[champion]["key"],
        )
        champions_object[champion] = champion_object

    DBHandler.create_update_champion(champion_object)
