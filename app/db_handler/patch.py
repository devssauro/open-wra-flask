from flask import Request

from app.mod_tournament.models import MatchupMap
from app.mod_view.utils import filter_map_data


class PatchHandler:
    @staticmethod
    def get_patches(request: Request) -> list[str]:
        query = (
            MatchupMap.query.with_entities(MatchupMap.patch)
            .filter(
                *filter_map_data(request, "patch"),
                MatchupMap.patch.isnot(None),
            )
            .distinct()
            .order_by(MatchupMap.patch)
        )
        return [p.patch for p in query]
