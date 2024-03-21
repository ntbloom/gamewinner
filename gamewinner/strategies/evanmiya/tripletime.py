from gamewinner.strategies.istrategy import IStrategy
from gamewinner.strategies.evanmiya.vanilla_miya import VanillaMiya
from gamewinner.team import Team


class Tripletime(IStrategy):
    """
    Uses all default IEvanMiyaStrategy methods
    self._team_metric() returns overal Evan Miya rank
    """

    @property
    def name(self) -> str:
        return "Tripletime"

    def prepare(self, teams: dict[str, Team]) -> None:
        self.em = IEvanMiya()
        self.em.prepare(teams)

        

    def _team_metric(self, team: Team) -> float:
        props = self.em.get_props(team)
        return self.em._rank_to_percentile(props.rank)
