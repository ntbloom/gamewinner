from gamewinner.games.bracket import Bracket


class TestStrategies:
    def test_the_final_game_happens(self, strategized_bracket: Bracket) -> None:
        strategized_bracket.play()
        assert strategized_bracket.winner
        assert strategized_bracket.runner_up
