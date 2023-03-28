from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class FireWaterFireWater(IEvanMiyaStrategy):
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
            self._rank_to_percentile(props.def_rank)
            - 0.75 * props.kill_shots_allowed_per_game
            + 0.75 * props.kill_shots_per_game
            + 0.75 * self._rank_to_percentile(props.injury_rank)
            + 0.25 * self._rank_to_percentile(props.home_rank, reverse=True)
        )
        return overall_score

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 76, 70
