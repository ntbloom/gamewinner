from typing import Any

from gamewinner.bracket.bracket import Bracket, RegionalBracket
from gamewinner.printers.iprinter import IPrinter
from gamewinner.teams.team import Team


class PlainText(IPrinter):
    name = "text"

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
        for region in bracket.regions:
            cls._region(region)
        cls._final_four(bracket)
        print()
        print(f"[red]{len(bracket.upsets)} upsets predicted:")
        for upset in bracket.upsets:
            print(f"[red]\t{upset}")

    @classmethod
    def _region(cls, region: RegionalBracket) -> None:
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
