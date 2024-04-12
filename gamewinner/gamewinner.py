import gamewinner.printers as printers
import gamewinner.strategies as strategies
from gamewinner.bracket.bracket import Bracket


def play(
    strategy: strategies.Strategy,
    year: int,
    printer: printers.Printer,
) -> None:
    bracket = Bracket(year)
    bracket.play(strategy)
    printer.print(bracket)
