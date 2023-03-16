from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class FireWaterFireWater(IEvanMiyaStrategy):
    """
    Uses all default IEvanMiyaStrategy methods
    self._team_metric() returns overal Evan Miya rank
    """

    @property
    def name(self) -> str:
        return "FireWaterFireWater"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        return self._rank_to_percentile(team.evanmiyaRank)
