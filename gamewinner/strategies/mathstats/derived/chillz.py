from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy
from gamewinner.teams.team import Team


class Chillz(IMathStatsStrategy):
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
            self._rank_to_percentile(props.rank_overall)
            + (props.rank_overall / 25)  # scaling based on a very good BPR (:shrug:)
            + props.obj_kills_per_game
            - props.obj_kills_concede_per_game
            * self._rank_to_percentile(props.rank_roster)
        )
        return overall_score


class KillerChillz(IMathStatsStrategy):
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
            self._rank_to_percentile(props.rank_overall)
            + (props.rank_overall / 25)  # scaling based on a very good BPR (:shrug:)
            + 3 * props.obj_kills_per_game
            - 3
            * props.obj_kills_concede_per_game
            * self._rank_to_percentile(props.rank_roster)
        )
        return overall_score
