import pytest

from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.scoring import BracketProvider, Providers
from gamewinner.strategies import BestRankWins, Strategy, WorstRankWins

"""
2024 cumulative scoring

BestRankWins 2024:
    First Round: 21 games
    Secound Round: 12 games
    Sweet Sixteen: 3 games
    Elite Eight: 2 games
    Final Four: 1 games
    Winner: correct
WorstRankWins 2024:
    0 points
WorstRankWins 2023:
    First Round: 2 games
    Second Round: 1 game
"""


@pytest.mark.xfail
@pytest.mark.parametrize(
    "year,basic_strategy,provider,expected_score",
    [
        (
            2024,
            BestRankWins(),
            Providers.espn,
            (10 * 21 + 20 * 12 + 40 * 3 + 80 * 2 + 160 * 1 + 320),
        ),
        (2024, WorstRankWins(), Providers.espn, 0),
        (2023, WorstRankWins(), Providers.espn, 2 * 10 + 20),
    ],
)
def test_bracket_scoring(
    year: int, basic_strategy: Strategy, provider: BracketProvider, expected_score: int
) -> None:
    bracket = Bracket(year)
    bracket.predict(basic_strategy)

    assert bracket.score(provider) == expected_score
