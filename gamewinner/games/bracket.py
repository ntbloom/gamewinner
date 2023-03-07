from gamewinner.games.region import Region
from gamewinner.strategies.istrategy import IStrategy
from gamewinner.team import GeographicRegion


class Bracket:
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

        self.regions = tuple(region.value.lower() for region in GeographicRegion)

        self.strategy = strategy

    def _play_round(self, round_name: str) -> None:
        self.strategy.adjust()
        for reg in self.regions:
            cmd = f"self.{reg}.{round_name}()"
            eval(cmd)

    def _first_round(self) -> None:
        self._play_round("first_round")

    def _second_round(self) -> None:
        self._play_round("second_round")

    def _sweet_sixteen(self) -> None:
        self._play_round("sweet_sixteen")

    def _elite_eight(self) -> None:
        self._play_round("elite_eight")

    def _final_four(self) -> None:
        # west plays east
        self.winner_west_east, self.loser_west_east = self.strategy.pick(
            self.west.winner, self.east.winner
        )
        # south plays midwest
        self.winner_south_midwest, self.loser_south_midwest = self.strategy.pick(
            self.south.winner, self.midwest.winner
        )

    def _final(self) -> None:
        self.strategy.adjust()
        self.winner, self.runner_up = self.strategy.pick(
            self.winner_west_east, self.winner_south_midwest
        )
        self.final_score = self.strategy.predict_score(self.winner, self.runner_up)

    def play(self) -> None:
        self.strategy.prepare()
        self._first_round()

        self.strategy.adjust()
        self._second_round()

        self.strategy.adjust()
        self._sweet_sixteen()

        self.strategy.adjust()
        self._elite_eight()

        self.strategy.adjust()
        self._final_four()

        self.strategy.adjust()
        self._final()

    def print(self) -> None:
        """Print the bracket on the page"""
        pass
