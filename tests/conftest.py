import pytest
from _pytest.python import Metafunc

from gamewinner.strategies import BestRankWins, Strategy, available_strategies


def pytest_generate_tests(metafunc: Metafunc) -> None:
    strategy_fixture = "strategy"
    if strategy_fixture in metafunc.fixturenames:
        metafunc.parametrize(
            strategy_fixture,
            available_strategies,
            scope="function",
            ids=[strategy.name for strategy in available_strategies],
        )


# @pytest.fixture(scope="class")
# def reference_year() -> int:
#     return 2022
#
#
# @pytest.fixture(scope="class")
# def this_year() -> int:
#     return 2024
#
#
@pytest.fixture(scope="class")
def best_wins() -> Strategy:
    return BestRankWins()


#
#
# @pytest.fixture(scope="class")
# def worst_wins_bracket(reference_year: int) -> Bracket:
#     return Bracket(WorstRankWins(), reference_year)
#
#
# @pytest.fixture(scope="function")
# def strategized_bracket(strategy: Strategy, this_year: int) -> Bracket:
#     # don't worry about breaking changes and only run strategies for this year
#     return Bracket(strategy, this_year)
