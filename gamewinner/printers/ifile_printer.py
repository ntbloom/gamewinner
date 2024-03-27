import os
from pathlib import Path
from typing import Any, TextIO

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers.iprinter import IPrinter


class IFilePrinter(IPrinter):
    @classmethod
    def print(cls, bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        dest_dir = Path(__file__).parent.parent.joinpath("generated")
        filename = dest_dir.joinpath(f"{bracket.strategy.name}-{bracket.year.year}.bkt")
        if filename.exists():
            os.remove(filename)
        with open(filename, "w+") as f:
            cls._print(bracket, f)

    @classmethod
    def _print(cls, bracket: Bracket, file_desc: TextIO) -> None:
        raise NotImplementedError
