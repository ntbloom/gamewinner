from __future__ import annotations

import csv
from abc import ABC
from pathlib import Path
from random import randint
from statistics import median
from typing import Callable, NamedTuple

from gamewinner.strategies.istrategy import IStrategy
from gamewinner.teams.team import Team, get_definitive_name

STATS_FILE = Path(__file__).parent.joinpath("data").joinpath("mathstats2024.csv")


class MSProps(NamedTuple):
    # rankings
    rank_overall: int
    rank_offense: int
    rank_defense: int
    rank_tempo: int
    rank_injury: int
    rank_home: int
    rank_roster: int

    # derived scores
    raw_overall: float
    raw_offense: float
    raw_defense: float
    raw_tempo: float

    # adjustments
    adjust_opponent: float
    adjust_pace: float

    # objective scores
    obj_kills_per_game: float
    obj_kills_concede_per_game: float
    obj_kills_total: int
    obj_kills_conceded_total: int
    obj_wins: int
    obj_losses: int

    # deprecated
    resume_rank: int = -1


class IMathStatsStrategy(IStrategy, ABC):
    """
    Class for strategies using statistical math data

    The only thing you _have to_ implement is self._team_metric()
    """

    stat_teams: dict[str, MSProps]

    def prepare(self, teams: dict[str, Team]) -> None:
        """
        Loads all the data and attaches it to the teams
        """
        assert STATS_FILE.exists()
        self.stat_teams = {}

        with open(STATS_FILE, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                (
                    rank_overall,
                    name,
                    raw_offense,
                    raw_defense,
                    raw_overall,
                    adjust_opponent,
                    adjust_pace,
                    rank_offense,
                    rank_defense,
                    raw_tempo,
                    rank_tempo,
                    rank_injury,
                    rank_home,
                    rank_roster,
                    obj_kills_per_game,
                    obj_kills_concede_per_game,
                    obj_kills_total,
                    obj_kills_conceded_total,
                    obj_wins,
                    obj_losses,
                ) = row

                # add stats to relevant team if they're in the tournament
                name = get_definitive_name(name)
                if name in teams:
                    props = MSProps(
                        rank_overall=int(rank_overall),
                        raw_offense=float(raw_offense),
                        raw_defense=float(raw_defense),
                        raw_overall=float(raw_overall),
                        adjust_opponent=float(adjust_opponent),
                        adjust_pace=float(adjust_pace),
                        rank_offense=int(rank_offense),
                        rank_defense=int(rank_defense),
                        raw_tempo=float(raw_tempo),
                        rank_tempo=int(rank_tempo),
                        rank_injury=int(rank_injury),
                        rank_home=int(rank_home),
                        rank_roster=int(rank_roster),
                        obj_kills_per_game=float(obj_kills_per_game),
                        obj_kills_concede_per_game=float(obj_kills_concede_per_game),
                        obj_kills_total=int(obj_kills_total),
                        obj_kills_conceded_total=int(obj_kills_conceded_total),
                        obj_wins=int(obj_wins),
                        obj_losses=int(obj_losses),
                    )
                    self.stat_teams[str(name)] = props

    def _team_metric(self, team: Team) -> float:
        raise NotImplementedError

    #########
    # everything below here can be overriden, or you can inherit the defaults
    #########

    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        return randint(70, 78), randint(61, 69)

    def pick(self, team1: Team, team2: Team) -> Team:
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
            return team1
        else:
            self._log.debug(f"----- {team2} wins")
            return team2

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

    def get_props(self, team: Team) -> MSProps:
        return self.stat_teams[team.name]
