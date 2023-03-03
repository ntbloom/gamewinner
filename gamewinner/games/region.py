from gamewinner.strategies import Strategy
from gamewinner.team import Team


class Region:
    def __init__(self, teams: list[Team], wildcards: list[Team], strategy: Strategy):
        assert len(wildcards) == 2
        assert len(teams) == 16
        self.teams = teams
        self.teams.sort(key=lambda x: x.rank_reg)

        self.strategy = strategy
        self._g0 = self.strategy.pick(wildcards[0], wildcards[1])

        # round 1
        self.g1 = self._pick(1, 16)
        self.g2 = self._pick(8, 9)
        self.g3 = self._pick(5, 12)
        self.g4 = self._pick(4, 13)
        self.g5 = self._pick(6, 11)
        self.g6 = self._pick(3, 14)
        self.g7 = self._pick(7, 10)
        self.g8 = self._pick(2, 15)

        # round 2
        self.g9 = self.strategy.pick(self.g1, self.g2)
        self.g10 = self.strategy.pick(self.g3, self.g4)
        self.g11 = self.strategy.pick(self.g5, self.g6)
        self.g12 = self.strategy.pick(self.g7, self.g8)

        # sweet 16
        self.g13 = self.strategy.pick(self.g9, self.g10)
        self.g14 = self.strategy.pick(self.g11, self.g12)

        # elite 8
        self.g15 = self.strategy.pick(self.g13, self.g14)
        self.winner = self.g15

    def print(self) -> None:
        col0 = 0
        col1 = 12
        col2 = 20
        col3 = 35
        print(" " * col0, self.g1.name)
        print(" " * col1, self.g9.name)
        print(" " * col0, self.g2.name)
        print(" " * col2, self.g13.name)
        print(" " * col0, self.g3.name)
        print(" " * col1, self.g10.name)
        print(" " * col0, self.g4.name)
        print(" " * col3, self.g15.name)
        print(" " * col0, self.g5.name)
        print(" " * col1, self.g11.name)
        print(" " * col0, self.g6.name)
        print(" " * col2, self.g14.name)
        print(" " * col0, self.g7.name)
        print(" " * col1, self.g12.name)
        print(" " * col0, self.g8.name)

    def _pick(self, one: int, two: int) -> Team:
        return self.strategy.pick(self.teams[one - 1], self.teams[two - 1])
