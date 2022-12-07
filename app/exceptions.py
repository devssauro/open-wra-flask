class DraftIntegrityError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LineupIntegrityError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GlobalBanError(Exception):
    def __init__(self, message: str, team_id: int, champion_id: int):
        self.message = message
        self.team_id = team_id
        self.champion_id = champion_id
        super().__init__(self.message)
