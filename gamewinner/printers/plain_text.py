from typing import Any

from gamewinner.games.bracket import Bracket, Region
from gamewinner.printers.iprinter import IPrinter
from gamewinner.team import Team


class PlainText(IPrinter):
    name = "PlainText"

    @staticmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        PlainText._print(bracket)

    @classmethod
    def _print(cls, bracket: Bracket) -> None:
        print(
            f"Overall prediction for {bracket.strategy.name}/{bracket.year.year}: "
            f"{bracket.winner} over {bracket.runner_up}: "
            f"{bracket.final_score}"
        )
        print()
        cls._first_four(bracket)
        for region in bracket.regions:
            cls._region(region)
        cls._final_four(bracket)

    @classmethod
    def _first_four(cls, bracket: Bracket) -> None:
        print("FIRST FOUR:")
        for game in bracket.first_four:
            cls._print_game(*game)

    @classmethod
    def _region(cls, region: Region) -> None:
        print(region.name.value.upper() + ":")
        indentations = 0
        for i in range(1, 16):
            if i == 9 or i == 13 or i == 15:
                indentations += 1

            winner: Team = eval(f"region.w{i}")
            loser: Team = eval(f"region.l{i}")
            cls._print_game(winner, loser, indentations)

    @classmethod
    def _final_four(cls, bracket: Bracket) -> None:
        print("FINAL FOUR:")
        cls._print_game(bracket.ff2_winner, bracket.ff2_loser)
        cls._print_game(bracket.ff1_winner, bracket.ff1_loser)
        print("FINAL:")
        cls._print_game(bracket.winner, bracket.runner_up)

    @classmethod
    def _print_game(cls, winner: Team, loser: Team, indentation: int = 0) -> None:
        tabs = indentation * "\t"
        print(f" {tabs}{winner} beats {loser}")
