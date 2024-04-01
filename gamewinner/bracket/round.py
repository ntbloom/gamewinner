from __future__ import annotations

from enum import IntEnum, unique


@unique
class Round(IntEnum):
    FIRST_ROUND = 1
    SECOND_ROUND = 2
    SWEET_SIXTEEN = 3
    ELITE_EIGHT = 4
    FINAL_FOUR = 5
    FINALS = 6
    WINNER = 7
