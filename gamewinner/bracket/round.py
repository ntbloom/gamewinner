from __future__ import annotations

from enum import IntEnum, unique


@unique
class Round(IntEnum):
    FirstRound = 1
    SecondRound = 2
    SweetSixteen = 3
    EliteEight = 4
    FinalFour = 5
    Finals = 6
    Winner = 7
