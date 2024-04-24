import gamewinner.printers as printers
import gamewinner.strategies as strategies
from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.scoring import BracketProvider
from gamewinner.strategies import available_strategies


def play(
    strategy: strategies.Strategy,
    year: int,
    printer: printers.Printer,
) -> None:
    bracket = Bracket(year)
    bracket.predict(strategy)
    printer.print(bracket)


def rank_brackets(year: int, provider: BracketProvider) -> None:
    scores = []
    for strategy in available_strategies:
        bracket = Bracket(year)
        bracket.predict(strategy)
        scores.append((bracket.score(provider), strategy.name))

    scores.sort(key=lambda x: x[0], reverse=True)
    for score in scores:
        print(f"{score[1]}: {score[0]} points")
