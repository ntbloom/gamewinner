import gamewinner.printers as printers
import gamewinner.strategies as strategies
from gamewinner.games.bracket import Bracket
from gamewinner.years import Year, available_years, this_year


def play(
    strategy: strategies.Strategy,
    year: int = this_year.year,
    printer: printers.Printer = printers.WithColors,
) -> None:
    def _find_year() -> Year:
        for _year in available_years:
            if _year.year == year:
                return _year
        raise ValueError(f"Unsupported year: {year}")

    bracket = Bracket.create(strategy, _find_year())
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
        default=this_year.year,
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
    play(strategy, year, printer)


if __name__ == "__main__":
    main()
