from app.mod_tournament.models import MatchupMap
from app.mod_view.utils import filter_map_data_v2


class PatchHandler:
    """Database handler for Patch operations"""

    @staticmethod
    def get_patches(tournament: list[int] | int, team: list[int] | int) -> list[str]:
        """Returns a list of Patches for the given request"""
        query = (
            MatchupMap.query.with_entities(MatchupMap.patch)
            .filter(
                *filter_map_data_v2(tournament=tournament, team=team),
                MatchupMap.patch.isnot(None),
            )
            .distinct()
            .order_by(MatchupMap.patch)
        )
        return [p.patch for p in query]
