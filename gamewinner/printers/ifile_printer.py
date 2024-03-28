import os
from pathlib import Path
from typing import Any, TextIO

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers.iprinter import IPrinter


class IFilePrinter(IPrinter):
    extension: str = NotImplemented

    @classmethod
    def print(cls, bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        dest_dir = Path(__file__).parent.parent.parent.joinpath("generated")
        filename = dest_dir.joinpath(
            f"{bracket.strategy.name}-{bracket.year.year}-{cls.name}.{cls.extension}"
        )
        if filename.exists():
            os.remove(filename)
        with open(filename, "w+") as f:
            cls._print(f, bracket)

    @classmethod
    def _print(cls, fd: TextIO, bracket: Bracket) -> None:
        raise NotImplementedError
