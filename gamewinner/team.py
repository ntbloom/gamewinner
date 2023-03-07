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
        regional_rank: int,
        national_rank: int,
        **kwargs: Any,
    ):
        self.name = name
        self.region = region
        self.rank_reg = regional_rank
        self.rank_nat = national_rank
        for k, v in kwargs.items():
            setattr(self, f"_{k}", v)

    def __repr__(self) -> str:
        return f"name={self.name}, region={self.region.value}, reg_rank={self.rank_reg}, nat_rank={self.rank_nat}"  # noqa
