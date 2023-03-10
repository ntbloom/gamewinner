from pathlib import Path

import pytest
from _pytest.python import Metafunc

from gamewinner.games.bracket import Bracket
from gamewinner.strategies import (
    BestRankWins,
    SlothfireSteady,
    Strategy,
    VanillaMiya,
    WorstRankWins,
)
from gamewinner.team import Team


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
        available_strategies = (
            BestRankWins(),
            WorstRankWins(),
            VanillaMiya(),
            SlothfireSteady(),
        )
        metafunc.parametrize(fixture, available_strategies, scope="function")


@pytest.fixture(scope="function")
def strategized_bracket(teamfile: Path, strategy: Strategy) -> Bracket:
    bracket = Bracket.create(teamfile, strategy)
    bracket.play()
    return bracket


best_worst = (
    ("Notre Dame", "Rutgers"),
    ("Texas A&M-Corpus Christi", "Texas Southern"),
    ("Bryant", "Wright State"),
    ("Wyoming", "Indiana"),
)


class TestBracketBestWins:
    def test_print_team(self, best_wins_bracket: Bracket) -> None:
        best_wins_bracket.play()
        print(best_wins_bracket.winner)

    @pytest.mark.parametrize("winner,loser", best_worst)
    def test_playoffs(
        self, best_wins_bracket: Bracket, winner: Team, loser: Team
    ) -> None:
        bracket = best_wins_bracket
        bracket.play()

        teams = {
            team.name
            for team in bracket.west.teams
            + bracket.east.teams
            + bracket.south.teams
            + bracket.midwest.teams
        }
        assert winner in teams
        assert loser not in teams

    def test_bracket_with_best_wins(self, best_wins_bracket: Bracket) -> None:
        bracket = best_wins_bracket
        bracket.play()

        # should be all #1s
        assert bracket.west.winner.name == "Gonzaga"
        assert bracket.east.winner.name == "Baylor"
        assert bracket.south.winner.name == "Arizona"
        assert bracket.midwest.winner.name == "Kansas"

        assert bracket.winner.name == "Arizona"
        assert bracket.runner_up.name == "Gonzaga"


class TestBracketWorstWins:
    @pytest.mark.parametrize("best,worst", best_worst)
    def test_playoffs(
        self, worst_wins_bracket: Bracket, best: Team, worst: Team
    ) -> None:
        bracket = worst_wins_bracket
        bracket.play()

        teams = {
            team.name
            for team in bracket.west.teams
            + bracket.east.teams
            + bracket.south.teams
            + bracket.midwest.teams
        }
        assert worst in teams
        assert best not in teams

    def test_bracket_with_best_wins(self, worst_wins_bracket: Bracket) -> None:
        bracket = worst_wins_bracket
        bracket.play()

        # should be all #1s
        assert bracket.west.winner.name == "Georgia State"
        assert bracket.east.winner.name == "Norfolk State"
        assert bracket.south.winner.name == "Wright State"
        assert bracket.midwest.winner.name == "Texas Southern"

        assert bracket.winner.name == "Texas Southern"
        assert bracket.runner_up.name == "Georgia State"


class TestStrategiesArePlayable:
    def test_the_final_game_happens(self, strategized_bracket: Bracket) -> None:
        assert strategized_bracket.winner
        assert strategized_bracket.runner_up
