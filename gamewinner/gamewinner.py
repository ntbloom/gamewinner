from pathlib import Path

from gamewinner.games.bracket import Bracket
from gamewinner.strategies import Strategy


def play(year: int, strategy: Strategy) -> None:
    teamfile = Path(__file__).parent.joinpath("data").joinpath(f"{year}.csv")
    bracket = Bracket.create(teamfile, strategy)
    bracket.play()
