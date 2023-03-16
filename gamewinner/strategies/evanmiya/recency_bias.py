import random
from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy2
from gamewinner.team import Team


class RecencyBias(IEvanMiyaStrategy2):
    """
    RecencyBias looks to reward teams playing their best basketball in the 30
    days leading up to the tournament. 
    
    Still heavily based on BPR, however the results will be influenced by each 
    team's recent play.
    """

    @property
    def name(self) -> str:
        return "RecencyBias"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            random.random()
            * self._rank_to_percentile(team.evanmiyaResumeRank)
            * team.evanmiyaBPR
        )

        # recency factor
        overall_score = overall_score + (
            0.5
            * random.random()
            * team.evanmiyaBPRChange
        )

        return overall_score


class RecencyBiasDumBayz(IEvanMiyaStrategy2):
    """
    The Bayesian version of RecencyBias
    Simulates the core strategy 1000 times and takes the median,
    then modifies it with the upset score.
    """

    @property
    def name(self) -> str:
        return "RecencyBiasDumBayz"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = self._dumbayz(
            lambda: (
                random.random()
                * self._rank_to_percentile(team.evanmiyaResumeRank)
                * team.evanmiyaBPR
            )
        )

        # recency factor
        overall_score = overall_score + (
            0.5
            * random.random()
            * team.evanmiyaBPRChange
        )

        return overall_score
