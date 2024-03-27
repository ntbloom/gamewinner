import random

from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy
from gamewinner.teams.team import Team


class SlothfireSteady(IMathStatsStrategy):
    """
    Using math data and heavily weighting teams that play slow
      and don't let other teams go on runs against them.

    In theory, this would pick UVa high, but we'll see what the numbers say...
    """

    @property
    def name(self) -> str:
        return "SlothfireSteady"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.rank_defense)
            + 0.5 * self._rank_to_percentile(props.rank_tempo, reverse=True)
            + 0.3 * self._rank_to_percentile(props.rank_offense)
            + 0.3 * self._rank_to_percentile(props.rank_overall)
            - props.obj_kills_concede_per_game
        )

        # upset factor
        overall_score = overall_score + random.random() * (
            self._rank_to_percentile(props.rank_roster)
            + min(self._rank_to_percentile(props.rank_home, reverse=True), 0.5)
        )

        return overall_score


class SlothfireSteadiest(IMathStatsStrategy):
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
            self._rank_to_percentile(props.rank_defense)
            + 0.5 * self._rank_to_percentile(props.rank_tempo, reverse=True)
            + 0.3 * self._rank_to_percentile(props.rank_offense)
            + 0.3 * self._rank_to_percentile(props.rank_overall)
            - props.obj_kills_concede_per_game
        )

        # upset factor
        overall_score = overall_score + (
            self._rank_to_percentile(props.rank_roster)
            + min(self._rank_to_percentile(props.rank_home, reverse=True), 0.5)
        )

        return overall_score


class SlothfireSteadyBayz(IMathStatsStrategy):
    """
    Same thing, but with 100 iterations of DumBayz for added steadiness
    """

    @property
    def name(self) -> str:
        return "SlothfireSteadyBayz"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        overall_score = (
            self._rank_to_percentile(props.rank_defense)
            + 0.5 * self._rank_to_percentile(props.rank_tempo, reverse=True)
            + 0.3 * self._rank_to_percentile(props.rank_offense)
            + 0.3 * self._rank_to_percentile(props.rank_overall)
            - props.obj_kills_concede_per_game
        )

        # upset factor
        overall_score = overall_score + self._dumbayz(
            lambda: (
                random.random()
                * (
                    self._rank_to_percentile(props.rank_roster)
                    + min(
                        self._rank_to_percentile(props.rank_home, reverse=True),
                        0.5,
                    )
                )
            ),
            numdraws=100,
        )

        return overall_score
