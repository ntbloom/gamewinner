import random
from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class TheCuts23(IEvanMiyaStrategy):
    """
    The Inuagural Effort by The Mind Behind The Cuts, Dan H Cook III

    Heavily based on BPR, but with a large randomness factor added as well

    Additional weighting on Resume Rank and a little extra random bonus
    weighted on the inverse of Home Rank (i.e. you get a slight penalty
    for being significantly better at home than on the road)
    """

    @property
    def name(self) -> str:
        return "TheCuts23"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            random.random()
            * self._rank_to_percentile(team.evanmiyaResumeRank)
            * team.evanmiyaBPR
        )

        # upset factor
        overall_score = overall_score + (
            0.5
            * random.random()
            * self._rank_to_percentile(team.evanmiyaHomeRank, reverse=True)
        )

        return overall_score


class TheCuts23Frozen(IEvanMiyaStrategy):
    """
    TheCuts23 without any randomness.

    Final Four pick for 2023 below.


    """

    @property
    def name(self) -> str:
        return "TheCuts23Frozen"

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 82, 68

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            self._rank_to_percentile(team.evanmiyaResumeRank) * team.evanmiyaBPR
        )

        # upset factor
        overall_score = overall_score + (
            0.5 * self._rank_to_percentile(team.evanmiyaHomeRank, reverse=True)
        )

        return overall_score


class TheCuts23DumBayz(IEvanMiyaStrategy):
    """
    The Bayesian version of TheCuts23

    Simulates the core strategy 1000 times and takes the median,
    then modifies it with the upset score.
    """

    @property
    def name(self) -> str:
        return "TheCuts23DumBayz"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = self._dumbayz(
            lambda: (
                random.random()
                * self._rank_to_percentile(team.evanmiyaResumeRank)
                * team.evanmiyaBPR
            )
        )

        # upset factor
        overall_score = overall_score + (
            0.5
            * random.random()
            * self._rank_to_percentile(team.evanmiyaHomeRank, reverse=True)
        )

        return overall_score
