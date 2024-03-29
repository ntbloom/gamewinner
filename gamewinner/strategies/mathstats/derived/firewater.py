from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy
from gamewinner.teams.team import Team


class FireWaterFireWater(IMathStatsStrategy):
    """
    SJB likes teams that play D and can get hot and go on a run.
    Also, you gotta be able to play on the road.
    """

    @property
    def name(self) -> str:
        return "FireWaterFireWater"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.rank_defense)
            - 0.75 * props.obj_kills_concede_per_game
            + 0.75 * props.obj_kills_per_game
            + 0.75 * self._rank_to_percentile(props.rank_injury)
            + 0.25 * self._rank_to_percentile(props.rank_home, reverse=True)
        )
        return overall_score

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 76, 70
