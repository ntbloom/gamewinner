from gamewinner.bracket.bracket import Bracket


class TestStrategies:
    def test_the_final_game_happens(self, strategized_bracket: Bracket) -> None:
        assert strategized_bracket.winner
        assert strategized_bracket.runner_up
