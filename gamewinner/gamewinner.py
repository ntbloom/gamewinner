import gamewinner.printers as printers
import gamewinner.strategies as strategies
from gamewinner.games.bracket import Bracket
from gamewinner.years import Year


def play(
    strategy: strategies.Strategy,
    year: Year,
    printer: printers.Printer,
) -> None:
    bracket = Bracket.create(strategy, year)
    bracket.play()
    printer.print(bracket)
