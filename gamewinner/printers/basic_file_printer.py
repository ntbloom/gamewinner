from typing import TextIO

from gamewinner.bracket.bracket import Bracket, RegionalBracket
from gamewinner.printers.ifile_printer import IFilePrinter
from gamewinner.teams.team import Team


class BasicFilePrinter(IFilePrinter):
    name = "basic"
    extension = "txt"

    @classmethod
    def _print(cls, fd: TextIO, bracket: Bracket) -> None:
        fd.write(
            f"Overall prediction for {bracket.strategy.name}/{bracket.year.year}:\n"
            f"{bracket.winner} over {bracket.runner_up}: {bracket.final_score}\n\n"
        )
        for region in bracket.regions:
            cls._region(fd, region)
        cls._final_four(fd, bracket)
        fd.write(f"\n\n{len(bracket.upsets)} upsets predicted:")
        for upset in bracket.upsets:
            fd.write(upset)

    @classmethod
    def _region(cls, fd: TextIO, region: RegionalBracket) -> None:
        fd.write(region.name.value.upper() + ":\n")
        indentations = 0
        for i in range(1, 16):
            if i == 9 or i == 13 or i == 15:
                indentations += 1

            winner: Team = eval(f"region.w{i}")
            loser: Team = eval(f"region.l{i}")
            cls._print_game(fd, winner, loser, indentations)

    @classmethod
    def _final_four(cls, fd: TextIO, bracket: Bracket) -> None:
        fd.write("\nFINAL FOUR:\n")
        cls._print_game(fd, bracket.ff2_winner, bracket.ff2_loser)
        cls._print_game(fd, bracket.ff1_winner, bracket.ff1_loser)
        fd.write("\nFINAL:\n")
        cls._print_game(fd, bracket.winner, bracket.runner_up)

    @classmethod
    def _print_game(
        cls, fd: TextIO, winner: Team, loser: Team, indentation: int = 0
    ) -> None:
        tabs = indentation * "\t"
        fd.write(f" {tabs}{winner} beats {loser}\n")
