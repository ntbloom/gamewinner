from __future__ import annotations

import csv
from pathlib import Path

from gamewinner.games.region import Region
from gamewinner.strategies.istrategy import Strategy
from gamewinner.team import GeographicRegion, Team


class Bracket:
    def __init__(
        self,
        first_four: list[tuple[Team, Team]],
        west: Region,
        east: Region,
        south: Region,
        midwest: Region,
        strategy: Strategy,
        west_final_four_matchup: GeographicRegion,
    ):
        self.played = False

        self.first_four = first_four
        self.west = west
        self.east = east
        self.south = south
        self.midwest = midwest

        self._west_machup = west_final_four_matchup

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
        self.regions = (self.west, self.east, self.south, self.midwest)

        self.strategy = strategy

    @property
    def teams(self) -> dict[str, Team]:
        return self._teams

    @property
    def final_four(self) -> tuple[tuple[Team, Team], ...]:
        return tuple(self._final_four)

    @staticmethod
    def create(
        teamfile: Path, strategy: Strategy, west_final_four_matchup: GeographicRegion
    ) -> Bracket:
        assert teamfile.exists(), f"Illegal file: {str(teamfile)}"

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

        # play the playoffs, add the teams to the regions accordingly
        playoffs.sort(key=lambda team: team.region.value)
        first_four: list[tuple[Team, Team]] = []
        for order in [
            (0, 1),
            (2, 3),
            (4, 5),
            (6, 7),
        ]:
            first_four.append(strategy.pick(playoffs[order[0]], playoffs[order[1]]))
        for t in first_four:
            eval(f"{t[0].region.value.lower()}_teams.append(t[0])")

        west = Region(GeographicRegion.WEST, west_teams, strategy)
        east = Region(GeographicRegion.EAST, east_teams, strategy)
        south = Region(GeographicRegion.SOUTH, south_teams, strategy)
        midwest = Region(GeographicRegion.MIDWEST, midwest_teams, strategy)

        return Bracket(
            first_four, west, east, south, midwest, strategy, west_final_four_matchup
        )

    def _play_round(self, round_name: str) -> None:
        self.strategy.adjust(self.teams)
        for reg in self._region_names:
            cmd = f"self.{reg}.{round_name}()"
            eval(cmd)

    def _play_first_round(self) -> None:
        self._play_round("first_round")

    def _play_second_round(self) -> None:
        self._play_round("second_round")

    def _play_sweet_sixteen(self) -> None:
        self._play_round("sweet_sixteen")

    def _play_elite_eight(self) -> None:
        self._play_round("elite_eight")

    def _play_final_four(self) -> None:
        # decide the matchups based on who the west bracket is matched against
        matchups = {
            "east": self.east.winner,
            "south": self.south.winner,
            "midwest": self.midwest.winner,
        }
        west_opponent = matchups.pop(self._west_machup.name.lower())
        self.ff1_winner, self.ff1_loser = self.strategy.pick(
            self.west.winner, west_opponent
        )
        self.ff2_winner, self.ff2_loser = self.strategy.pick(
            matchups.popitem()[1], matchups.popitem()[1]
        )
        self._final_four = (self.ff1_winner, self.ff1_loser), (
            self.ff2_winner,
            self.ff2_loser,
        )

    def _play_final(self) -> None:
        self.strategy.adjust(self.teams)
        self.winner, self.runner_up = self.strategy.pick(
            self.ff1_winner, self.ff2_winner
        )
        self.final_score = self.strategy.predict_score(self.winner, self.runner_up)

    def play(self) -> None:
        self._play_first_round()
        self._play_second_round()
        self._play_sweet_sixteen()
        self._play_elite_eight()
        self._play_final_four()
        self._play_final()
        self.played = True
