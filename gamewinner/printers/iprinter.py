from abc import ABC, abstractmethod
from typing import Any

from gamewinner.games.bracket import Bracket


class IPrinter(ABC):
    name: str = NotImplemented

    @staticmethod
    @abstractmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        pass


Printer = IPrinter
