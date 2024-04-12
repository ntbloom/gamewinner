import pytest

from gamewinner.bracket.bracket import Bracket
from gamewinner.strategies.istrategy import Strategy
from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy


class TestStrategies:
    def test_every_strategy_plays_to_completion(
        self, test_year: int, strategy: Strategy
    ) -> None:
        if test_year == 2023 and isinstance(strategy, IMathStatsStrategy):
            pytest.skip("2023 mathstats data is incompatible")

        bracket = Bracket(test_year)
        bracket.play(strategy)
        assert bracket.winner
