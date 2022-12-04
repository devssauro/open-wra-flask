from app.mod_tournament.models import Champion


class ChampionHandler:
    """Database handler for Champion operations"""

    @staticmethod
    def get_champions() -> list[Champion]:
        """Return all champions from database"""
        query = Champion.query.all()
        return query
