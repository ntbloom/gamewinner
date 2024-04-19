from gamewinner.bracket.bracket import Bracket


class TestStrategies:
    def test_every_strategy_plays_to_completion(
        self, strategized_bracket: Bracket
    ) -> None:
        assert strategized_bracket.winner
