from typing import Any

from gamewinner.games.bracket import Bracket
from gamewinner.printers.iprinter import IPrinter


class PdfBracket(IPrinter):
    name = "PdfBracket"

    @staticmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError
