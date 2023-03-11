from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class TheCuts23(IEvanMiyaStrategy):
    """
    Uses all default IEvanMiyaStrategy methods
    self._team_metric() returns overal Evan Miya rank
    """

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        # metric1 <- function(team, bpr, resume, home_rank) {
        # overall_score <- runif(1) * rank_to_percentile(resume) * bpr
        # overall_score <- overall_score + (0.5 * runif(1) * rank_to_percentile(home_rank, reverse = T))
        # return(overall_score)

