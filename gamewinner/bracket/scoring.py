from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from gamewinner.bracket.stage import Stage


class BracketProvider(NamedTuple):
    name: str
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

    def __str__(self) -> str:
        return f"BracketProvider({self.name})"


@dataclass
class Providers:
    espn = BracketProvider("espn", 10, 20, 40, 80, 160, 320)
    yahoo = BracketProvider("yahoo", 1, 2, 4, 8, 16, 32)
    cbs = BracketProvider("cbs", 1, 2, 4, 8, 16, 32)
    fox_sports = BracketProvider("foxsports", 1, 2, 4, 8, 16, 32)
    ncaa_dot_com = BracketProvider("ncaa.com", 1, 2, 4, 8, 16, 32)
    balanced = BracketProvider("balanced", 1, 2, 3, 4, 6, 10)


available_providers = (
    Providers.espn,
    Providers.yahoo,
    Providers.cbs,
    Providers.fox_sports,
    Providers.ncaa_dot_com,
    Providers.balanced,
)
