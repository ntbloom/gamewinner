from pathlib import Path

import gamewinner.printers as printers
import gamewinner.strategies as strategies
from gamewinner.games.bracket import Bracket


def play(year: int, strategy: strategies.Strategy, printer: printers.Printer) -> None:
    teamfile = Path(__file__).parent.parent.joinpath("data").joinpath(f"{year}.csv")
    bracket = Bracket.create(teamfile, strategy)
    bracket.play()
    printer.print(bracket)


def main() -> None:
    import argparse

    legal_printers = [printer.name for printer in printers.available_printers]
    legal_strategies = [strategy.name for strategy in strategies.available_strategies]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strategy",
        type=str,
        default="BestRankWins",
        help=f"what strategy you want to use, must be one of {legal_strategies}",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2023,
        help="year you want to play",
    )
    parser.add_argument(
        "--printer",
        type=str,
        default="PlainText",
        help=f"how to print the bracket, must be one of {legal_printers}",
    )

    args = parser.parse_args()
    strategy: strategies.Strategy
    printer: printers.Printer
    year: int = args.year

    try:
        strategy = eval(f"strategies.{args.strategy}()")
    except NameError:
        raise ValueError(
            f"Unsupported strategy {args.strategy}, legal choices = {legal_strategies}"
        )
    try:
        printer = eval(f"printers.{args.printer}")
    except NameError:
        raise ValueError(
            f"Unsupported printer {args.printer}, legal choices = {legal_printers}"
        )
    play(year, strategy, printer)


if __name__ == "__main__":
    main()
