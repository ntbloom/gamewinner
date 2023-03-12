import random
from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class SlothfireSteady(IEvanMiyaStrategy):
    """
    Using Evan Miya data and heavily weighting teams that play slow
      and don't let other teams go on runs against them.

    In theory, this would pick UVa high, but we'll see what the numbers say...
    """

    @property
    def name(self) -> str:
        return "SlothFireSteady"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            self._rank_to_percentile(team.evanmiyaDefRank)
            + 0.5 * self._rank_to_percentile(team.evanmiyaTempoRank, reverse=True)
            + 0.3 * self._rank_to_percentile(team.evanmiyaOffRank)
            + 0.3 * self._rank_to_percentile(team.evanmiyaRank)
            - team.evanmiyaKillShotsAllowedPerGame
        )

        # upset factor
        overall_score = overall_score + random.random() * (
            self._rank_to_percentile(team.evanmiyaResumeRank)
            + min(self._rank_to_percentile(team.evanmiyaHomeRank, reverse=True), 0.5)
        )

        return overall_score
