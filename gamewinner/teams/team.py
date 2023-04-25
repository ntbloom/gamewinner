from typing import Any

from gamewinner.bracket.geographic_region import GeographicRegion
from gamewinner.teams.alternate_names import name_map


def get_definitive_name(raw: str) -> str:
    """
    Get a definitive name for each team so we can pull from different data sets"""
    definitive = name_map.get(raw.lower(), None)
    if not definitive:
        raise ValueError(f"Can't find definitive name for `{raw}`")
    return definitive


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
        self.name = get_definitive_name(name)
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
