from typing import TextIO

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers.ifile_printer import IFilePrinter


class BasicFilePrinter(IFilePrinter):
    @classmethod
    def _print(cls, bracket: Bracket, file_desc: TextIO) -> None:
        file_desc.write(f"{bracket.winner=}\n")
        file_desc.write(f"{bracket.runner_up=}\n")
