import random

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.teams.team import Team


class SlothfireSteady(IEvanMiyaStrategy):
    """
    Using Evan Miya data and heavily weighting teams that play slow
      and don't let other teams go on runs against them.

    In theory, this would pick UVa high, but we'll see what the numbers say...
    """

    @property
    def name(self) -> str:
        return "SlothfireSteady"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.def_rank)
            + 0.5 * self._rank_to_percentile(props.tempo_rank, reverse=True)
            + 0.3 * self._rank_to_percentile(props.off_rank)
            + 0.3 * self._rank_to_percentile(props.rank)
            - props.kill_shots_allowed_per_game
        )

        # upset factor
        overall_score = overall_score + random.random() * (
            self._rank_to_percentile(props.resume_rank)
            + min(self._rank_to_percentile(props.home_rank, reverse=True), 0.5)
        )

        return overall_score


class SlothfireSteadiest(IEvanMiyaStrategy):
    """
    Same thing, but with no randomness.

    For 2023, this is the Final Four that it picks. Not bad.

    FINAL FOUR:
        (1) Purdue beats (4) Virginia
        (1) Houston beats (2) UCLA
    FINAL:
        (1) Houston beats (1) Purdue

    """

    @property
    def name(self) -> str:
        return "SlothfireSteadiest"

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return 76, 67

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.def_rank)
            + 0.5 * self._rank_to_percentile(props.tempo_rank, reverse=True)
            + 0.3 * self._rank_to_percentile(props.off_rank)
            + 0.3 * self._rank_to_percentile(props.rank)
            - props.kill_shots_allowed_per_game
        )

        # upset factor
        overall_score = overall_score + (
            self._rank_to_percentile(props.resume_rank)
            + min(self._rank_to_percentile(props.home_rank, reverse=True), 0.5)
        )

        return overall_score


class SlothfireSteadyBayz(IEvanMiyaStrategy):
    """
    Same thing, but with 100 iterations of DumBayz for added steadiness
    """

    @property
    def name(self) -> str:
        return "SlothfireSteadyBayz"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.def_rank)
            + 0.5 * self._rank_to_percentile(props.tempo_rank, reverse=True)
            + 0.3 * self._rank_to_percentile(props.off_rank)
            + 0.3 * self._rank_to_percentile(props.rank)
            - props.kill_shots_allowed_per_game
        )

        # upset factor
        overall_score = overall_score + self._dumbayz(
            lambda: (
                random.random()
                * (
                    self._rank_to_percentile(props.resume_rank)
                    + min(
                        self._rank_to_percentile(props.home_rank, reverse=True),
                        0.5,
                    )
                )
            ),
            numdraws=100,
        )

        return overall_score
