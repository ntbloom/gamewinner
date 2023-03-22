from __future__ import annotations

import csv
from abc import ABC
from pathlib import Path
from random import randint
from statistics import median
from typing import Callable, NamedTuple

from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import Team

EVAN_MIYA_FILE = Path(__file__).parent.joinpath("data").joinpath("evanmiya.csv")


class EMProps(NamedTuple):
    rank: int
    obpr: float
    dbpr: float
    bpr: float
    off_rank: int
    def_rank: int
    true_tempo: float
    tempo_rank: int
    injury_rank: int
    roster_rank: int
    kill_shots_per_game: float
    kill_shots_allowed_per_game: float
    total_kill_shots: int
    total_kill_shots_allowed: int
    resume_rank: int
    home_rank: int


class IEvanMiyaStrategy(IStrategy, ABC):
    """
    Class for strategies using Evan Miya data

    The only thing you _have to_ implement is self._team_metric()
    """

    em_teams: dict[str, EMProps]

    def prepare(self, teams: dict[str, Team]) -> None:
        """
        Loads all the Evan Miya data and attaches it to the teams
        """
        assert EVAN_MIYA_FILE.exists()
        self.em_teams = {}

        with open(EVAN_MIYA_FILE, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                (
                    name,
                    rank,
                    obpr,
                    dpbr,
                    bpr,
                    off_rank,
                    def_rank,
                    true_tempo,
                    tempo_rank,
                    injury_rank,
                    roster_rank,
                    kill_shots_per_game,
                    kill_shots_allowed_per_game,
                    total_kill_shots,
                    total_kill_shots_allowed,
                    resume_rank,
                    home_rank,
                ) = row

                # add all Evan Miya stats to relevant team if they're in the tournament
                if name in teams:
                    props = EMProps(
                        rank=int(rank),
                        obpr=float(obpr),
                        dbpr=float(dpbr),
                        bpr=float(bpr),
                        off_rank=int(off_rank),
                        def_rank=int(def_rank),
                        true_tempo=float(true_tempo),
                        tempo_rank=int(tempo_rank),
                        injury_rank=int(injury_rank),
                        roster_rank=int(roster_rank),
                        kill_shots_per_game=float(kill_shots_per_game),
                        kill_shots_allowed_per_game=float(kill_shots_allowed_per_game),
                        total_kill_shots=int(total_kill_shots),
                        total_kill_shots_allowed=int(total_kill_shots_allowed),
                        resume_rank=int(resume_rank),
                        home_rank=int(home_rank),
                    )
                    self.em_teams[str(name)] = props

    def _team_metric(self, team: Team) -> float:
        raise NotImplementedError

    #########
    # everything below here can be overriden, or you can inherit the defaults
    #########

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return randint(70, 78), randint(61, 69)

    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        """
        By default, this picks the team with the higher self._team_metric() score
        """
        team1_overall = self._team_metric(team1)
        team2_overall = self._team_metric(team2)

        self._log.debug(f"----- {team1} vs. {team2}")
        self._log.debug(f"{team1}: {team1_overall}")
        self._log.debug(f"{team2}: {team2_overall}")
        if team1_overall > team2_overall:
            self._log.debug(f"----- {team1} wins")
            return team1, team2
        else:
            self._log.debug(f"----- {team2} wins")
            return team2, team1

    def _rank_to_percentile(self, rank: int, reverse: bool = False) -> float:
        perc = max((251 - rank) / 250, 0)
        if reverse:
            perc = 1 - perc
        return perc

    def _dumbayz(self, func: Callable, numdraws: int = 1000) -> float:
        """
        A dumb Bayesian simulator.

        Runs func() numdraws times and returns the median from all the runs

        func -- a function that returns a float, i.e. a _team_metric() function)
        numdraws -- number of times to run func(), defaults to 1000
        """
        ans = median([func() for x in range((numdraws - 1))])
        return float(ans)
