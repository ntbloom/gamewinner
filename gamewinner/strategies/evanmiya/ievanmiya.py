import csv
from abc import ABC, abstractmethod
from pathlib import Path
from random import randint
from typing import Callable
from statistics import median

from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import Team

EVAN_MIYA_FILE = (
    Path(__file__).parent.joinpath("data").joinpath("evanmiya_clean_20230309.csv")
)


class IEvanMiyaStrategy(IStrategy, ABC):
    """
    Class for strategies using Evan Miya data

    The only thing you _have to_ implement is self._team_metric()
    """

    def prepare(self, teams: dict[str, Team]) -> None:
        """
        Loads all the Evan Miya data and attaches it to the teams
        """
        assert EVAN_MIYA_FILE.exists()

        with open(EVAN_MIYA_FILE, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                (
                    name,
                    evanmiyaRank,
                    evanmiyaOBPR,
                    evanmiyaDBPR,
                    evanmiyaBPR,
                    evanmiyaOffRank,
                    evanmiyaDefRank,
                    evanmiyaTrueTempo,
                    evanmiyaTempoRank,
                    evanmiyaInjuryRank,
                    evanmiyaRosterRank,
                    evanmiyaKillShotsPerGame,
                    evanmiyaKillShotsAllowedPerGame,
                    evanmiyaTotalKillShots,
                    evanmiyaTotalKillShotsAllowed,
                    evanmiyaResumeRank,
                    evanmiyaHomeRank,
                ) = row

                # add all Evan Miya stats to relevant team if they're in the tournament
                if name in teams:
                    team = teams[name]
                    setattr(team, "evanmiyaRank", int(evanmiyaRank))
                    setattr(team, "evanmiyaOBPR", float(evanmiyaOBPR))
                    setattr(team, "evanmiyaDBPR", float(evanmiyaDBPR))
                    setattr(team, "evanmiyaBPR", float(evanmiyaBPR))
                    setattr(team, "evanmiyaOffRank", int(evanmiyaOffRank))
                    setattr(team, "evanmiyaDefRank", int(evanmiyaDefRank))
                    setattr(team, "evanmiyaTrueTempo", float(evanmiyaTrueTempo))
                    setattr(team, "evanmiyaTempoRank", int(evanmiyaTempoRank))
                    setattr(team, "evanmiyaInjuryRank", int(evanmiyaInjuryRank))
                    setattr(team, "evanmiyaRosterRank", int(evanmiyaRosterRank))
                    setattr(
                        team,
                        "evanmiyaKillShotsPerGame",
                        float(evanmiyaKillShotsPerGame),
                    )
                    setattr(
                        team,
                        "evanmiyaKillShotsAllowedPerGame",
                        float(evanmiyaKillShotsAllowedPerGame),
                    )
                    setattr(team, "evanmiyaTotalKillShots", int(evanmiyaTotalKillShots))
                    setattr(
                        team,
                        "evanmiyaTotalKillShotsAllowed",
                        int(evanmiyaTotalKillShotsAllowed),
                    )
                    setattr(team, "evanmiyaResumeRank", int(evanmiyaResumeRank))
                    setattr(team, "evanmiyaHomeRank", int(evanmiyaHomeRank))

        for team in teams.values():
            # make sure we found every team and added evanmiya attrs.
            # could check all of them, but for now just check one.
            assert hasattr(team, "evanmiyaRank"), f"skipped {team.name}"

    @abstractmethod
    def _team_metric(self, team: Team) -> float:
        return NotImplemented

    #########
    # everything below here can be overriden, or you can inherit the defaults
    #########

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return random.randint(70, 78), random.randint(61, 69)

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

    def _dumbayz(self, func: Callable, numdraws: int = 1000) -> :
        """
        A dumb Bayesian simulator.

        Runs func() numdraws times and returns the median from all the runs

        func -- a function that returns a float, i.e. a _team_metric() function)
        numdraws -- number of times to run func(), defaults to 1000
        """
        return median([func() for x in range((numdraws - 1))])
