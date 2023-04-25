from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.teams.team import Team


class Chillz(IEvanMiyaStrategy):
    """
    The Chillz, not to be confused with Mr Freeze.

    Option A: Scaling BPR and adding them all together
    """

    @property
    def name(self) -> str:
        return "Chillz"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.rank)
            + (props.bpr / 25)  # scaling based on a very good BPR (:shrug:)
            + props.kill_shots_per_game
            - props.kill_shots_allowed_per_game
            * self._rank_to_percentile(props.roster_rank)
        )
        return overall_score


class KillerChillz(IEvanMiyaStrategy):
    """
    The Chillz, not to be confused with Mr Freeze.

    Option B: Same
    """

    @property
    def name(self) -> str:
        return "KillerChillz"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.rank)
            + (props.bpr / 25)  # scaling based on a very good BPR (:shrug:)
            + 3 * props.kill_shots_per_game
            - 3
            * props.kill_shots_allowed_per_game
            * self._rank_to_percentile(props.roster_rank)
        )
        return overall_score
