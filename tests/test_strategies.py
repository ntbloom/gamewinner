from gamewinner.bracket.bracket import Bracket
from gamewinner.strategies.istrategy import Strategy


class TestStrategies:
    def test_every_strategy_plays_to_completion(self, strategy: Strategy) -> None:
        bracket = Bracket(2024)
        bracket.play(strategy)
        assert bracket.winner
