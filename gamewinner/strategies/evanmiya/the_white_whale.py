from __future__ import annotations

import random
from dataclasses import dataclass
from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


@dataclass
class EMProps:
    @no_type_check
    def __init__(self, team: Team):
        self._team = team
        random.seed(1851)

        self.team_name: str = self._team.name
        self.obpr: float = team.evanmiyaOBPR
        self.dbpr: float = team.evanmiyaDBPR
        self.bpr: float = team.evanmiyaBPR
        self.true_tempo: float = team.evanmiyaTrueTempo

        self.kill_shots_per_game: int = team.evanmiyaKillShotsPerGame
        self.kill_shots_allowed_per_game: int = team.evanmiyaKillShotsAllowedPerGame
        self.total_kill_shots: int = team.evanmiyaTotalKillShots
        self.total_kill_shots_allowed: int = team.evanmiyaTotalKillShotsAllowed

        self.rank: int = team.evanmiyaRank
        self.off_rank: int = team.evanmiyaOffRank
        self.def_rank: int = team.evanmiyaDefRank
        self.tempo_rank: int = team.evanmiyaTempoRank
        self.roster_rank: int = team.evanmiyaRosterRank
        self.injury_rank: int = team.evanmiyaInjuryRank
        self.resume_rank: int = team.evanmiyaResumeRank
        self.home_rank: int = team.evanmiyaHomeRank

    def __str__(self) -> str:
        return self.team_name

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, EMProps):
            return NotImplemented

        fave: EMProps
        underdog: EMProps
        fave, underdog = (self, other) if self.rank < other.rank else (other, self)
        upset = False

        # can an underdog with good defense stifle a better team?
        tempo_winner, tempo_loser = (
            (fave, underdog) if fave.tempo_rank < other.tempo_rank else (underdog, fave)
        )
        defense_holds = True if (tempo_winner.obpr < tempo_loser.dbpr) else False
        if defense_holds and tempo_winner == self:
            upset = True

        if upset:
            return underdog == self
        else:
            return fave == self

    def __ge__(self, other: object) -> bool:
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        return NotImplemented

    def __le__(self, other: object) -> bool:
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EMProps):
            return NotImplemented
        return self.team_name == other.team_name  # type: ignore


class TheWhiteWhale(IEvanMiyaStrategy):
    """
    Witness the white bear of the poles, and the white shark of the tropics;
    what but their smooth, flaky whiteness makes them the transcendent horrors
    they are?
    """

    @property
    def name(self) -> str:
        return "TheWhiteWhale"

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        props1 = EMProps(team1)
        props2 = EMProps(team2)

        if props1 > props2:
            return team1, team2
        else:
            return team2, team1
