from _pytest.python import Metafunc

from gamewinner.games.bracket import Bracket
from gamewinner.strategies import available_strategies


def pytest_generate_tests(metafunc: Metafunc) -> None:
    fixture = "strategy"
    if fixture in metafunc.fixturenames:
        metafunc.parametrize(fixture, available_strategies, scope="function")


class TestStrategies:
    def test_the_final_game_happens(self, strategized_bracket: Bracket) -> None:
        assert strategized_bracket.winner
        assert strategized_bracket.runner_up
