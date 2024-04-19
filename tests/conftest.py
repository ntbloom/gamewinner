import pytest
from _pytest.python import Metafunc

from gamewinner.bracket.bracket import Bracket
from gamewinner.strategies import available_strategies
from gamewinner.strategies.istrategy import Strategy
from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy


def pytest_generate_tests(metafunc: Metafunc) -> None:
    strategy_fixture = "strategy"
    if strategy_fixture in metafunc.fixturenames:
        metafunc.parametrize(
            strategy_fixture,
            available_strategies,
            scope="function",
            ids=[strategy.name for strategy in available_strategies],
        )

    year_fixture = "test_year"
    testable_years = (
        2023,
        2024,
    )
    if year_fixture in metafunc.fixturenames:
        metafunc.parametrize(
            year_fixture, testable_years, scope="function", ids=testable_years
        )


@pytest.fixture(scope="function")
def strategized_bracket(strategy: Strategy, test_year: int) -> Bracket:
    # don't worry about breaking changes and only run strategies for this year
    if test_year == 2023 and isinstance(strategy, IMathStatsStrategy):
        pytest.skip("2023 mathstats data is incompatible")

    bracket = Bracket(test_year)
    bracket.play(strategy)
    return bracket
