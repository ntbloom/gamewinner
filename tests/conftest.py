from pathlib import Path

import pytest
from _pytest.python import Metafunc

from gamewinner.games.bracket import Bracket
from gamewinner.strategies import (
    BestRankWins,
    Strategy,
    WorstRankWins,
    available_strategies,
)


@pytest.fixture(scope="class")
def teamfile() -> Path:
    """Test team file to use"""
    games2022 = Path(__file__).parent.parent.joinpath("data").joinpath("2022.csv")
    assert games2022.exists()
    return games2022


@pytest.fixture(scope="class")
def best_wins_bracket(teamfile: Path) -> Bracket:
    return Bracket.create(teamfile, BestRankWins())


@pytest.fixture(scope="class")
def worst_wins_bracket(teamfile: Path) -> Bracket:
    return Bracket.create(teamfile, WorstRankWins())


def pytest_generate_tests(metafunc: Metafunc) -> None:
    fixture = "strategy"
    if fixture in metafunc.fixturenames:
        metafunc.parametrize(fixture, available_strategies, scope="function")


@pytest.fixture(scope="function")
def strategized_bracket(teamfile: Path, strategy: Strategy) -> Bracket:
    bracket = Bracket.create(teamfile, strategy)
    bracket.play()
    return bracket
