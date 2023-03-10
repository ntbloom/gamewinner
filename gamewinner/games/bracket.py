from __future__ import annotations

import csv
from pathlib import Path

from gamewinner.games.region import Region
from gamewinner.strategies.istrategy import Strategy
from gamewinner.team import GeographicRegion, Team


class Bracket:
    def __init__(
        self,
        west: Region,
        east: Region,
        south: Region,
        midwest: Region,
        strategy: Strategy,
    ):
        self.west = west
        self.east = east
        self.south = south
        self.midwest = midwest

        self._teams = {
            team.name: team
            for team in (
                self.west.teams
                + self.east.teams
                + self.south.teams
                + self.midwest.teams
            )
        }
        self._region_names = tuple(region.value.lower() for region in GeographicRegion)

        self.strategy = strategy

    @property
    def teams(self) -> dict[str, Team]:
        return self._teams

    @staticmethod
    def create(teamfile: Path, strategy: Strategy) -> Bracket:
        assert teamfile.exists()

        west_teams: list[Team] = []
        east_teams: list[Team] = []
        south_teams: list[Team] = []
        midwest_teams: list[Team] = []
        playoffs: list[Team] = []
        teams: dict[str, Team] = {}

        with open(teamfile, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                name, region, rank, wins, losses = row
                match region:
                    case _ if "Playoff" in region:
                        _region = region.split("-")[0]
                        in_playoff = True
                    case _:
                        _region = region
                        in_playoff = False
                geographic_region = GeographicRegion(str(_region))
                team = Team(
                    name=name,
                    region=geographic_region,
                    rank=int(rank),
                    wins=int(wins),
                    losses=int(losses),
                )
                teams[name] = team
                if in_playoff:
                    playoffs.append(team)
                else:
                    eval(f"{geographic_region.value.lower()}_teams.append(team)")

        # do any adjustments to the strategy now that we know who all the teams are
        strategy.prepare(teams)

        playoffs.sort(key=lambda team: team.region.value)
        first_playoff, _ = strategy.pick(playoffs[0], playoffs[1])
        second_playoff, _ = strategy.pick(playoffs[2], playoffs[3])
        third_playoff, _ = strategy.pick(playoffs[4], playoffs[5])
        fourt_playoff, _ = strategy.pick(playoffs[6], playoffs[7])
        for team in (first_playoff, second_playoff, third_playoff, fourt_playoff):
            eval(f"{team.region.value.lower()}_teams.append(team)")

        west = Region(GeographicRegion.WEST, west_teams, strategy)
        east = Region(GeographicRegion.EAST, east_teams, strategy)
        south = Region(GeographicRegion.SOUTH, south_teams, strategy)
        midwest = Region(GeographicRegion.MIDWEST, midwest_teams, strategy)

        return Bracket(west, east, south, midwest, strategy)

    def _play_round(self, round_name: str) -> None:
        self.strategy.adjust(self.teams)
        for reg in self._region_names:
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
        self.strategy.adjust(self.teams)
        self.winner, self.runner_up = self.strategy.pick(
            self.winner_west_east, self.winner_south_midwest
        )
        self.final_score = self.strategy.predict_score(self.winner, self.runner_up)

    def play(self) -> None:
        self._first_round()
        self._second_round()
        self._sweet_sixteen()
        self._elite_eight()
        self._final_four()
        self._final()
        self.print()

    def print(self) -> None:
        pass
