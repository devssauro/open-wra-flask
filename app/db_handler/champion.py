from app.mod_tournament.models import Champion


class ChampionHandler:
    @staticmethod
    def get_champions() -> list[Champion]:
        query = Champion.query.all()
        return query
