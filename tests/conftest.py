from pathlib import Path

import pytest
from _pytest.python import Metafunc

from gamewinner.games.bracket import Bracket
from gamewinner.strategies import BestRankWins, Strategy, WorstRankWins
from gamewinner.team import GeographicRegion


def pytest_generate_tests(metafunc: Metafunc) -> None:
    fixture = "year"
    if fixture in metafunc.fixturenames:
        metafunc.parametrize(
            fixture,
            ((2022, GeographicRegion.EAST), (2023, GeographicRegion.MIDWEST)),
            scope="class",
        )


@pytest.fixture(scope="class")
def reference_year() -> tuple[int, GeographicRegion]:
    return 2022, GeographicRegion.EAST


@pytest.fixture(scope="module")
def data_dir() -> Path:
    return Path(__file__).parent.parent.joinpath("data")


@pytest.fixture(scope="class")
def teamfile(reference_year: tuple[int, GeographicRegion], data_dir: Path) -> Path:
    """Test team file to use"""
    year, _ = reference_year
    games2022 = data_dir.joinpath(f"{year}.csv")
    assert games2022.exists()
    return games2022


@pytest.fixture(scope="class")
def best_wins_bracket(
    reference_year: tuple[int, GeographicRegion], teamfile: Path
) -> Bracket:
    _, west_plays = reference_year
    return Bracket.create(teamfile, BestRankWins(), west_plays)


@pytest.fixture(scope="class")
def worst_wins_bracket(
    reference_year: tuple[int, GeographicRegion], teamfile: Path
) -> Bracket:
    _, west_plays = reference_year
    return Bracket.create(teamfile, WorstRankWins(), west_plays)


@pytest.fixture(scope="function")
def strategized_bracket(
    year: tuple[int, GeographicRegion], data_dir: Path, strategy: Strategy
) -> Bracket:
    calendar_year, west_plays = year
    teamfile = data_dir.joinpath(f"{calendar_year}.csv")
    bracket = Bracket.create(teamfile, strategy, west_plays)
    bracket.play()
    return bracket
