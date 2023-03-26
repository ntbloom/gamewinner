from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class TheOwl(IEvanMiyaStrategy):
    """
    SJB likes teams that play D and can get hot and go on a run.
    Also, you gotta be able to play on the road.

    For the record, this is the original: https://github.com/ntbloom/gamewinner/pull/20/
    """

    @property
    def name(self) -> str:
        return "TheOwl"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        overall_score = (
            self._rank_to_percentile(team.evanmiyaDefRank)
            - 0.75 * team.evanmiyaKillShotsAllowedPerGame
            + 0.75 * team.evanmiyaKillShotsPerGame
            + 0.75 * self._rank_to_percentile(team.evanmiyaInjuryRank)
            + 0.75 * self._rank_to_percentile(team.evanmiyaHomeRank, reverse=True)
        )
        return overall_score

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 76, 70