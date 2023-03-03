from __future__ import annotations

from abc import ABC, abstractmethod
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return NotImplemented
        return self.name == other.name

    def __repr__(self) -> str:
        return f"name={self.name}, region={self.region.value}, reg_rank={self.rank_reg}, nat_rank={self.rank_nat}"


class Strategy(ABC):
    @abstractmethod
    def pick(self, team1: Team, team2: Team) -> Team:
        """Pick a game winner"""
        return NotImplemented

    @abstractmethod
    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        """Predict the score of a game"""
        return NotImplemented


class Region:
    def __init__(self, teams: list[Team], wildcards: list[Team], strategy: Strategy):
        assert len(wildcards) == 2
        assert len(teams) == 16
        self.teams = teams
        self.teams.sort(key=lambda x: x.rank_reg)

        self.strategy = strategy
        self._g0 = self.strategy.pick(wildcards[0], wildcards[1])

        # round 1
        self.g1 = self._pick(1, 16)
        self.g2 = self._pick(8, 9)
        self.g3 = self._pick(5, 12)
        self.g4 = self._pick(4, 13)
        self.g5 = self._pick(6, 11)
        self.g6 = self._pick(3, 14)
        self.g7 = self._pick(7, 10)
        self.g8 = self._pick(8, 15)

        # round 2
        self.g9 = self.strategy.pick(self.g1, self.g2)
        self.g10 = self.strategy.pick(self.g3, self.g4)
        self.g11 = self.strategy.pick(self.g5, self.g6)
        self.g12 = self.strategy.pick(self.g7, self.g8)

        # sweet 16
        self.g13 = self.strategy.pick(self.g9, self.g10)
        self.g14 = self.strategy.pick(self.g11, self.g12)

        # elite 8
        self.g15 = self.strategy.pick(self.g13, self.g14)
        self.winner = self.g15

    def print(self) -> None:
        col0 = 0
        col1 = 12
        col2 = 20
        col3 = 35
        print(" " * col0, self.g1.name)
        print(" " * col1, self.g9.name)
        print(" " * col0, self.g2.name)
        print(" " * col2, self.g13.name)
        print(" " * col0, self.g3.name)
        print(" " * col1, self.g10.name)
        print(" " * col0, self.g4.name)
        print(" " * col3, self.g15.name)
        print(" " * col0, self.g5.name)
        print(" " * col1, self.g11.name)
        print(" " * col0, self.g6.name)
        print(" " * col2, self.g14.name)
        print(" " * col0, self.g7.name)
        print(" " * col1, self.g12.name)
        print(" " * col0, self.g8.name)

    def _pick(self, one: int, two: int) -> Team:
        return self.strategy.pick(self.teams[one - 1], self.teams[two - 1])


class FinalFour:
    def __init__(
        self,
        west: Region,
        east: Region,
        south: Region,
        midwest: Region,
        strategy: Strategy,
    ):
        self.west = west
        self.east = east
        self.south = south
        self.midwest = midwest

        self.strategy = strategy

        # final 4
        self.semi1 = self.strategy.pick(self.west.winner, self.east.winner)
        self.semi2 = self.strategy.pick(self.south.winner, self.midwest.winner)
        self.winner = self.strategy.pick(self.semi1, self.semi2)
        self.second_place = self.semi1 if self.winner == self.semi2 else self.semi2
        self.final_score = self.strategy.predict_score(self.winner, self.second_place)
