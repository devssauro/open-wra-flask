from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.exceptions import GlobalBanError
from app.mod_tournament.models.matchup_map import MatchupMap
from db_config import Base


class Matchup(Base, SerializerMixin):
    """Class to a matchup in a tournament

    A matchup is the Best of 3/5/7.

    Attributes:
        phase (str): The phase of the tournament where that matchup occurred
        datetime (datetime): The date and the time in hours when the matchup happened
        mvp_id (str): The player's id MVP for the matchup
        tournament_id (str): The tournament's id
        team1_id (int): The first team's id
        team2_id (int): The second team's id
        vod_link (str): The vod link to the matches
    """

    __tablename__ = "matchup"
    serialize_only = (
        "id",
        "datetime",
        "mvp_id",
        "tournament_id",
        "team1_id",
        "team2_id",
        "vod_link",
        "bo_size",
    )

    def __int__(
        self,
        datetime,
        phase,
        mvp,
        team1,
        team2,
        vod_link,
        bo_size,
        with_global_ban,
        last_no_global_ban,
    ):
        self.datetime = datetime
        self.phase = phase
        self.mvp_id = mvp
        self.team1_id = team1
        self.team2_id = team2
        self.vod_link = vod_link
        self.bo_size = bo_size
        self.with_global_ban = with_global_ban
        self.last_no_global_ban = last_no_global_ban

    phase = Column(String)
    datetime = Column(DateTime)
    mvp_id = Column(Integer, ForeignKey("player.id"))
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    team1_id = Column(Integer, ForeignKey("team.id"))
    team1 = relationship("Team", foreign_keys=[team1_id], back_populates="matchups_1")
    team2_id = Column(Integer, ForeignKey("team.id"))
    team2 = relationship("Team", foreign_keys=[team2_id], back_populates="matchups_2")
    bo_size = Column(Integer)
    vod_link = Column(String)
    with_global_ban = Column(Boolean, default=False)
    last_no_global_ban = Column(Boolean, default=False)

    maps: list[MatchupMap] = relationship("MatchupMap", back_populates="matchup")

    def add_map(self, matchup_map: MatchupMap) -> None:
        """Verify if the matchup has global ban and if it has some conflict with last maps"""
        if self.with_global_ban:
            if self.team1 == matchup_map.blue_side:
                team1_picks = [
                    matchup_map.blue_pick_1,
                    matchup_map.blue_pick_2,
                    matchup_map.blue_pick_3,
                    matchup_map.blue_pick_4,
                    matchup_map.blue_pick_5,
                ]
                team2_picks = [
                    matchup_map.red_pick_1,
                    matchup_map.red_pick_2,
                    matchup_map.red_pick_3,
                    matchup_map.red_pick_4,
                    matchup_map.red_pick_5,
                ]
            else:
                team2_picks = [
                    matchup_map.blue_pick_1,
                    matchup_map.blue_pick_2,
                    matchup_map.blue_pick_3,
                    matchup_map.blue_pick_4,
                    matchup_map.blue_pick_5,
                ]
                team1_picks = [
                    matchup_map.red_pick_1,
                    matchup_map.red_pick_2,
                    matchup_map.red_pick_3,
                    matchup_map.red_pick_4,
                    matchup_map.red_pick_5,
                ]
            if (
                self.last_no_global_ban
                and matchup_map.map_number < self.bo_size
                or not self.last_no_global_ban
                and matchup_map.map_number == self.bo_size
            ):
                for pick in team1_picks:
                    if pick in self.all_team1_picks:
                        raise GlobalBanError(
                            f"Team {self.team1_id} can't pick this champion again",
                            self.team_1_id,
                            pick,
                        )
                for pick in team2_picks:
                    if pick in self.all_team2_picks:
                        raise GlobalBanError(
                            f"Team {self.team2_id} can't pick this champion again",
                            self.team_2_id,
                            pick,
                        )

    @property
    def all_team1_picks(self) -> list:
        picks = []
        for _map in self.maps:
            if _map.team1_id == _map.blue_side:
                picks.append(_map.blue_pick_1)
                picks.append(_map.blue_pick_2)
                picks.append(_map.blue_pick_3)
                picks.append(_map.blue_pick_4)
                picks.append(_map.blue_pick_5)
            else:
                picks.append(_map.red_pick_1)
                picks.append(_map.red_pick_2)
                picks.append(_map.red_pick_3)
                picks.append(_map.red_pick_4)
                picks.append(_map.red_pick_5)
        return picks

    @property
    def all_team2_picks(self) -> list:
        picks = []
        for _map in self.maps:
            if _map.team2_id == _map.blue_side:
                picks.append(_map.blue_pick_1)
                picks.append(_map.blue_pick_2)
                picks.append(_map.blue_pick_3)
                picks.append(_map.blue_pick_4)
                picks.append(_map.blue_pick_5)
            else:
                picks.append(_map.red_pick_1)
                picks.append(_map.red_pick_2)
                picks.append(_map.red_pick_3)
                picks.append(_map.red_pick_4)
                picks.append(_map.red_pick_5)
        return picks
