from typing import Any

from gamewinner.games.bracket import Bracket
from gamewinner.printers.iprinter import IPrinter


class PlainText(IPrinter):
    name = "PlainText"

    @staticmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        print("Not implemented yet but will be soon!")
