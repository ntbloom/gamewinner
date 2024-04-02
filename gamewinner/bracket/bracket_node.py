from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique

from gamewinner.teams.team import Team


@unique
class Round(IntEnum):
    FIRST_ROUND = 1
    SECOND_ROUND = 2
    SWEET_SIXTEEN = 3
    ELITE_EIGHT = 4
    FINAL_FOUR = 5
    FINALS = 6
    WINNER = 7


@dataclass
class BracketNode:
    round: Round
    parent: BracketNode | None = None
    left_child: BracketNode | None = None
    right_child: BracketNode | None = None
    team: Team | None = None

    built: bool = False

    def __repr__(self) -> str:
        return f"{self.round=}, {self.parent=}"


RANKS = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
