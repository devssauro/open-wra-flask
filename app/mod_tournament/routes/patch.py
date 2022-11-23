from flask import Blueprint, request

from ...mod_view.utils import filter_map_data
from ..models import MatchupMap

bp = Blueprint("patch", __name__, url_prefix="/")


@bp.get("/patch")
def get_patches():
    patches = (
        MatchupMap.query.with_entities(MatchupMap.patch)
        .filter(*filter_map_data(request, "patch"), MatchupMap.patch.isnot(None))
        .distinct()
        .order_by(MatchupMap.patch)
    )

    return {"patches": [p.patch for p in patches]}
