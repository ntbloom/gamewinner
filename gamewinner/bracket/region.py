from abc import ABC, abstractmethod
from enum import IntEnum, unique
from typing import Any, Self


@unique
class GeographicRegion(IntEnum):
    WEST = 0
    EAST = 1
    SOUTH = 2
    MIDWEST = 3


class Team:
    def __init__(
        self,
        name: str,
        region: GeographicRegion,
        regional_rank: int,
        national_rank: int,
        **kwargs: Any,
    ):
        self._name = name
        self._region = region
        self._regional_rank = regional_rank
        self._national_rank = national_rank
        for k, v in kwargs:
            setattr(self, f"_{k}", v)

    def __eq__(self, other: Self) -> bool:
        return self._name == other.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def national_rank(self) -> int:
        return self._national_rank

    @property
    def regional_rank(self) -> int:
        return self._regional_rank


class Strategy(ABC):
    @abstractmethod
    def pick(self, team1: Team, team2: Team) -> Team:
        """Pick a game winner"""
        return NotImplemented


class Region:
    def __init__(self, teams: list[Team]):
        self._teams = teams
        self._teams.sort(key=lambda x: x.regional_rank)

    def play(self, strategy: Strategy) -> None:
        """Play all the games according to a strategy"""
        pass


class Tournament:
    def __init__(self, west: Region, east: Region, south: Region, midwest: Region):
        self._west = west
        self._east = east
        self._south = south
        self._midwest = midwest
