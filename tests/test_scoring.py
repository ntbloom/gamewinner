import pytest

from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.exceptions import TournamentNotPlayedYetError
from gamewinner.bracket.scoring import BracketProvider, Providers
from gamewinner.strategies import BestRankWins, Strategy


@pytest.fixture(scope="function")
def provider() -> BracketProvider:
    return Providers.espn


@pytest.mark.parametrize("basic_strategy,expected_score", [(BestRankWins(), 100)])
def test_2024_scoring(
    basic_strategy: Strategy, provider: BracketProvider, expected_score: int
) -> None:
    bracket = Bracket(2024)
    bracket.play(basic_strategy)

    with pytest.raises(TournamentNotPlayedYetError):
        assert bracket.points

    bracket.score(provider)
    assert bracket.points == expected_score
