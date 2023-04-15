import pytest
from _pytest.python import Metafunc

from gamewinner.bracket.bracket import Bracket
from gamewinner.strategies import (
    BestRankWins,
    Strategy,
    WorstRankWins,
    available_strategies,
)
from gamewinner.bracket.years import Year, available_years, year2022


def pytest_generate_tests(metafunc: Metafunc) -> None:
    year_fixture = "every_year"
    if year_fixture in metafunc.fixturenames:
        metafunc.parametrize(
            year_fixture,
            available_years,
            scope="class",
            ids=[year.year for year in available_years],
        )

    strategy_fixture = "strategy"
    if strategy_fixture in metafunc.fixturenames:
        metafunc.parametrize(
            strategy_fixture,
            available_strategies,
            scope="function",
            ids=[strategy.name for strategy in available_strategies],
        )


@pytest.fixture(scope="class")
def reference_year() -> Year:
    return year2022


@pytest.fixture(scope="class")
def best_wins_bracket(reference_year: Year) -> Bracket:
    return Bracket.create(BestRankWins(), reference_year)


@pytest.fixture(scope="class")
def worst_wins_bracket(reference_year: Year) -> Bracket:
    return Bracket.create(WorstRankWins(), reference_year)


@pytest.fixture(scope="function")
def strategized_bracket(every_year: Year, strategy: Strategy) -> Bracket:
    bracket = Bracket.create(strategy, every_year)
    return bracket
