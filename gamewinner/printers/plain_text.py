from typing import Any

from gamewinner.games.bracket import Bracket, Region
from gamewinner.printers.iprinter import IPrinter
from gamewinner.team import Team


class PlainText(IPrinter):
    name = "PlainText"

    @staticmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        print(
            f"Overall prediction for {bracket.strategy.name}: "
            f"{bracket.winner} over {bracket.runner_up}: "
            f"{bracket.final_score}"
        )
        print()
        PlainText._first_four(bracket)
        for region in bracket.regions:
            PlainText._region(region)
        PlainText._final_four(bracket)

    @staticmethod
    def _first_four(bracket: Bracket) -> None:
        print("FIRST FOUR:")
        for game in bracket.first_four:
            PlainText._print_game(*game)

    @staticmethod
    def _region(region: Region) -> None:
        print(region.name.value.upper() + ":")
        indentations = 0
        for i in range(1, 16):
            if i == 9 or i == 13 or i == 15:
                indentations += 1

            winner: Team = eval(f"region.w{i}")
            loser: Team = eval(f"region.l{i}")
            PlainText._print_game(winner, loser, indentations)

    @staticmethod
    def _final_four(bracket: Bracket) -> None:
        print("FINAL FOUR:")
        PlainText._print_game(bracket.winner_south_midwest, bracket.loser_south_midwest)
        PlainText._print_game(bracket.winner_west_east, bracket.loser_west_east)
        print("FINAL:")
        PlainText._print_game(bracket.winner, bracket.runner_up)

    @staticmethod
    def _print_game(winner: Team, loser: Team, indentation: int = 0) -> None:
        tabs = indentation * "\t"
        print(f" {tabs}{winner} beats {loser}")
