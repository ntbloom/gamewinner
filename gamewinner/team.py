from enum import Enum, unique
from typing import Any


@unique
class GeographicRegion(Enum):
    WEST = "West"
    EAST = "East"
    SOUTH = "South"
    MIDWEST = "Midwest"


class Team:
    def __init__(
        self,
        name: str,
        region: GeographicRegion,
        rank: int,
        wins: int,
        losses: int,
        **kwargs: Any,
    ):
        self.name = name
        self.region = region
        self.rank = rank
        self.wins = wins
        self.losses = losses
        self.win_rate = self.wins / (self.wins + self.losses)
        for k, v in kwargs.items():
            setattr(self, f"_{k}", v)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"({self.rank}) {self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return NotImplemented
        return self.name == other.name
