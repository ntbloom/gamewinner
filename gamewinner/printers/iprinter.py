from abc import ABC, abstractmethod
from typing import Any, Type

from gamewinner.bracket.bracket import Bracket


class IPrinter(ABC):
    name: str = NotImplemented

    @staticmethod
    @abstractmethod
    def print(bracket: Bracket, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError


Printer = Type[IPrinter]
