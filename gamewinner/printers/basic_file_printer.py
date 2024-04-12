from typing import TextIO

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers.ifile_printer import IFilePrinter


class BasicFilePrinter(IFilePrinter):
    extension = "txt"
    name = "basic"

    @classmethod
    def _print(cls, fd: TextIO, bracket: Bracket) -> None:
        for game in bracket.games:
            fd.write(f"{str(game)}\n")
