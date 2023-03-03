from gamewinner.games.region import Region
from gamewinner.strategies.istrategy import IStrategy


class FinalFour:
    def __init__(
        self,
        west: Region,
        east: Region,
        south: Region,
        midwest: Region,
        strategy: IStrategy,
    ):
        self.west = west
        self.east = east
        self.south = south
        self.midwest = midwest

        self.strategy = strategy

        # final 4
        self.semi1 = self.strategy.pick(self.west.winner, self.east.winner)
        self.semi2 = self.strategy.pick(self.south.winner, self.midwest.winner)
        self.winner = self.strategy.pick(self.semi1, self.semi2)
        self.second_place = self.semi1 if self.winner == self.semi2 else self.semi2
        self.final_score = self.strategy.predict_score(self.winner, self.second_place)
