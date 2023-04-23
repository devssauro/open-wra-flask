from app.mod_tournament.models import Champion
from db_config import db


class ChampionHandler:
    """Database handler for Champion operations"""

    @staticmethod
    def get_champions() -> list[Champion]:
        """Return all champions from database"""
        query = Champion.query.all()
        return query

    @staticmethod
    def create_update_champion(champion: Champion) -> Champion:
        db.session.add(champion)
        db.session.commit()

        return champion
