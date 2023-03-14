from pathlib import Path

import gamewinner.printers as printers
import gamewinner.strategies as strategies
from gamewinner.games.bracket import Bracket
from gamewinner.team import GeographicRegion


def play(
    year: int,
    strategy: strategies.Strategy,
    west_final_four_matchup: GeographicRegion,
    printer: printers.Printer,
) -> None:
    teamfile = Path(__file__).parent.parent.joinpath("data").joinpath(f"{year}.csv")
    bracket = Bracket.create(teamfile, strategy, west_final_four_matchup)
    bracket.play()
    printer.print(bracket)


def main() -> None:
    import argparse

    legal_strategies = [strategy.name for strategy in strategies.available_strategies]
    legal_printers = {"plaintext", "color"}

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
        default="color",
        help=f"how to print the bracket, must be one of {legal_printers}",
    )

    args = parser.parse_args()
    strategy: strategies.Strategy
    year: int = args.year

    match year:
        case 2022:
            west_matchup = GeographicRegion.EAST
        case 2023:
            west_matchup = GeographicRegion.MIDWEST
        case _:
            raise ValueError("Unsupported year")

    try:
        strategy = eval(f"strategies.{args.strategy}()")
    except AttributeError:
        raise ValueError(
            f"Unsupported strategy {args.strategy}, legal choices = {legal_strategies}"
        )

    if args.printer not in legal_printers:
        raise ValueError(f"Unsupported printer, must be one of {legal_printers}")
    match args.printer:
        case "plaintext":
            printer = printers.PlainText
        case "color":
            printer = printers.WithColors
        case _:
            raise ValueError("illegal printer")
    play(year, strategy, west_matchup, printer)


if __name__ == "__main__":
    main()
