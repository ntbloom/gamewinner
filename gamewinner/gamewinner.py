from pathlib import Path

from gamewinner.games.bracket import Bracket
from gamewinner.strategies import (
    BestRankWins,
    SlothfireSteady,
    Strategy,
    VanillaMiya,
    WorstRankWins,
)


def play(year: int, strategy: Strategy) -> None:
    teamfile = Path(__file__).parent.parent.joinpath("data").joinpath(f"{year}.csv")
    bracket = Bracket.create(teamfile, strategy)
    bracket.play()
    bracket.print()


def main() -> None:
    import argparse

    available_strategies = (
        BestRankWins,
        SlothfireSteady,
        VanillaMiya,
        WorstRankWins,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strategy",
        type=str,
        default="BestRankWins",
        help="what strategy you want to use",
    )
    parser.add_argument("--year", type=int, default=2023, help="year you want to play")

    args = parser.parse_args()
    strategy: Strategy
    year: int = args.year

    try:
        strategy = eval(f"{args.strategy}()")
    except NameError:
        raise ValueError(
            f"Unsupported strategy {args.strategy}, must be in {available_strategies}"
        )
    play(year, strategy)


if __name__ == "__main__":
    main()
