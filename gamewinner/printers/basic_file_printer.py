from typing import TextIO

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers.ifile_printer import IFilePrinter


class BasicFilePrinter(IFilePrinter):
    extension = "txt"
    name = "basic"

    @classmethod
    def _print(cls, fd: TextIO, bracket: Bracket) -> None:

        gamestrings = []
        for game in bracket.games:
            gamestrings.append(f"{str(game)}\n")
        gamestrings.sort()
        gamestr: str
        for gamestr in gamestrings:
            indents = int(gamestr[1]) - 1
            fd.write(rf"{'\t' * indents}{gamestr}")  # flake8: noqa
