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

    def __repr__(self) -> str:
        return (
            f"{self.name}, "
            f"{self.region.value}, "
            f"#{self.rank}, "
            f"({self.wins}-{self.losses})/{round(self.win_rate*100)}%"
        )
