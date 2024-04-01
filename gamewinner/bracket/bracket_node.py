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
    parent: BracketNode | None
    left_child: BracketNode | None
    right_child: BracketNode | None
    team: Team | None = None
