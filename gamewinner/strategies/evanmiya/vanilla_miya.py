from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.teams.team import Team


class VanillaMiya(IEvanMiyaStrategy):
    """
    Uses all default IEvanMiyaStrategy methods
    self._team_metric() returns overal Evan Miya rank
    """

    @property
    def name(self) -> str:
        return "VanillaMiya"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        return self._rank_to_percentile(props.rank)
