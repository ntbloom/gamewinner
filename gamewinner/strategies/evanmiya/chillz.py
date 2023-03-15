from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class Chillz(IEvanMiyaStrategy):
    """
    The Chillz, not to be confused with Mr Freeze.

    Option A: Scaling BPR and adding them all together
    """

    @property
    def name(self) -> str:
        return "Chillz"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            self._rank_to_percentile(team.evanmiyaRank)
            + (team.evanmiyaBPR / 25) # scaling based on a very good BPR (:shrug:)
            + team.evanmiyaKillShotsPerGame 
            - team.evanmiyaKillShotsAllowedPerGame
            * self._rank_to_percentile(team.evanmiyaRosterRank)
            )
        return overall_score


class KillerChillz(IEvanMiyaStrategy):
    """
    The Chillz, not to be confused with Mr Freeze.

    Option B: Same
    """

    @property
    def name(self) -> str:
        return "KillerChillz"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            self._rank_to_percentile(team.evanmiyaRank)
            + (team.evanmiyaBPR / 25) # scaling based on a very good BPR (:shrug:)
            + 3 * team.evanmiyaKillShotsPerGame 
            - 3 * team.evanmiyaKillShotsAllowedPerGame
            * self._rank_to_percentile(team.evanmiyaRosterRank)
            )
        return overall_score

