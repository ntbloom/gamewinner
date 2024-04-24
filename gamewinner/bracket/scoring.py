from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from gamewinner.bracket.stage import Stage


class BracketProvider(NamedTuple):
    first_round_points: int
    second_round_points: int
    sweet_sixteen_points: int
    elite_eight_points: int
    final_four_points: int
    finals_points: int

    def stage_points(self, stage: Stage) -> int:
        match stage:
            case Stage.FirstRound:
                return self.first_round_points
            case Stage.SecondRound:
                return self.second_round_points
            case Stage.SweetSixteen:
                return self.sweet_sixteen_points
            case Stage.EliteEight:
                return self.elite_eight_points
            case Stage.FinalFour:
                return self.final_four_points
            case Stage.Finals:
                return self.finals_points
            case _:
                raise ValueError("must provide valid stage")


@dataclass
class Providers:
    espn = BracketProvider(10, 20, 40, 80, 160, 320)
    yahoo = BracketProvider(1, 2, 4, 8, 16, 32)
    cbs = BracketProvider(1, 2, 4, 8, 16, 32)
    fox_sports = BracketProvider(1, 2, 4, 8, 16, 32)
    ncaa_dot_com = BracketProvider(1, 2, 4, 8, 16, 32)
    balanced = BracketProvider(1, 2, 3, 4, 6, 10)
