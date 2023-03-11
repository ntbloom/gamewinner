from typing import no_type_check
import random

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class TheCuts23(IEvanMiyaStrategy):
    """
    Uses all default IEvanMiyaStrategy methods
    self._team_metric() returns overal Evan Miya rank
    """

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            random.random() *
            self._rank_to_percentile(team.evanmiyaResumeRank) * 
            team.evanmiyaBPR
        )

        # upset factor
        overall_score = (
            overall_score + (
                0.5 * 
                random.random() * 
                self._rank_to_percentile(team.evanmiyaHomeRank, reverse = T)
            )
        )
        
        return overall_score

