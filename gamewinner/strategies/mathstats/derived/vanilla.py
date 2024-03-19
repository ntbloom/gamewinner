from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy
from gamewinner.teams.team import Team


class Vanilla(IMathStatsStrategy):
    """
    Uses all default MathStatsStrategy methods
    self._team_metric() returns overal rank
    """

    @property
    def name(self) -> str:
        return "Vanilla"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        return self._rank_to_percentile(props.rank_overall)
