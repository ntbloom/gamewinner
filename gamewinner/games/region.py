import logging

from gamewinner.strategies import Strategy
from gamewinner.team import GeographicRegion, Team


class Region:
    def __init__(self, name: GeographicRegion, teams: list[Team], strategy: Strategy):
        self._log = logging.getLogger(__name__)
        self.name = name
        self.teams = teams
        self.teams.sort(key=lambda x: x.rank)

        self.strategy = strategy

        # do some quick checking
        assert len(teams) == 16, f"expected 16 teams, got {len(teams)}"
        ranks = {team.rank for team in self.teams}
        assert len(ranks) == 16, f"expected 16 unique ranks, got {len(ranks)}"

    def first_round(self) -> None:
        self._log.debug(f"{self.name.value} first round")

        def _pick(one: int, two: int) -> tuple[Team, Team]:
            return self._play(self.teams[one - 1], self.teams[two - 1])

        self.w1, self.l1 = _pick(1, 16)
        self.w2, self.l2 = _pick(8, 9)
        self.w3, self.l3 = _pick(5, 12)
        self.w4, self.l4 = _pick(4, 13)
        self.w5, self.l5 = _pick(6, 11)
        self.w6, self.l6 = _pick(3, 14)
        self.w7, self.l7 = _pick(7, 10)
        self.w8, self.l8 = _pick(2, 15)

    def second_round(self) -> None:
        self._log.debug(f"{self.name.value} second round")
        self.w9, self.l9 = self._play(self.w1, self.w2)
        self.w10, self.l10 = self._play(self.w3, self.w4)
        self.w11, self.l11 = self._play(self.w5, self.w6)
        self.w12, self.l12 = self._play(self.w7, self.w8)

    def sweet_sixteen(self) -> None:
        self._log.debug(f"{self.name.value} sweet sixteen")
        self.w13, self.l13 = self._play(self.w9, self.w10)
        self.w14, self.l14 = self._play(self.w11, self.w12)

    def elite_eight(self) -> None:
        self._log.debug(f"{self.name.value} elite eight")
        self.w15, self.l15 = self._play(self.w13, self.w14)
        self.winner = self.w15

    def _play(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        assert team1 is not None and team2 is not None
        return self.strategy.pick(team1, team2)
