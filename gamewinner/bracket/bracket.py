from __future__ import annotations

import csv
from pathlib import Path

from gamewinner.bracket.geographic_region import GeographicRegion
from gamewinner.bracket.regional_bracket import RegionalBracket
from gamewinner.bracket.years import Year, this_year
from gamewinner.strategies.istrategy import Strategy
from gamewinner.teams.team import Team


class InvalidDataFile(Exception):
    pass


class BracketLogicError(Exception):
    pass


class Bracket:
    def __init__(
        self,
        west: RegionalBracket,
        east: RegionalBracket,
        south: RegionalBracket,
        midwest: RegionalBracket,
        strategy: Strategy,
        year: Year = this_year,
    ):
        self.played = False

        self.west = west
        self.east = east
        self.south = south
        self.midwest = midwest

        self.year = year
        self._west_machup = year.west_plays

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
        self.upsets: list[str] = []
        self._winner: Team | None = None
        self._runner_up: Team | None = None

    @property
    def teams(self) -> dict[str, Team]:
        return self._teams

    @property
    def final_four(self) -> tuple[tuple[Team, Team], ...]:
        return tuple(self._final_four)

    @property
    def runner_up(self) -> Team:
        if not self._runner_up:
            raise BracketLogicError("must call `play()` first, or logic is broken")
        return self._runner_up

    @property
    def winner(self) -> Team:
        if not self._winner:
            raise BracketLogicError("must call `play()` first, or logic is broken")
        return self._winner

    @staticmethod
    def create(strategy: Strategy, year: Year) -> Bracket:
        teamfile = (
            Path(__file__)
            .parent.parent.parent.joinpath("data")
            .joinpath(f"{year.year}.csv")
        )
        assert teamfile.exists(), f"Missing teamfile for year {year.year}: {teamfile=}"

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
                try:
                    name, region, rank, wins, losses = row
                except ValueError:
                    raise InvalidDataFile(f"Bad entry for {row}")
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

        west = RegionalBracket(GeographicRegion.WEST, west_teams, strategy)
        east = RegionalBracket(GeographicRegion.EAST, east_teams, strategy)
        south = RegionalBracket(GeographicRegion.SOUTH, south_teams, strategy)
        midwest = RegionalBracket(GeographicRegion.MIDWEST, midwest_teams, strategy)

        return Bracket(west, east, south, midwest, strategy, year)

    def play(self) -> None:
        self.__play_first_round()
        self.__play_second_round()
        self.__play_sweet_sixteen()
        self.__play_elite_eight()
        self.__play_final_four()
        self.__play_final()
        self.played = True
        for region in self.regions:
            for upset in region.upsets:
                self.upsets.append(upset)

    def __play_round(self, round_name: str) -> None:
        for reg in self._region_names:
            cmd = f"self.{reg}.{round_name}()"
            eval(cmd)

    def __play_first_round(self) -> None:
        self.__play_round("first_round")

    def __play_second_round(self) -> None:
        self.__play_round("second_round")

    def __play_sweet_sixteen(self) -> None:
        self.__play_round("sweet_sixteen")

    def __play_elite_eight(self) -> None:
        self.__play_round("elite_eight")

    def __play_final_four(self) -> None:
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

    def __play_final(self) -> None:
        self._winner, self._runner_up = self.strategy.pick(
            self.ff1_winner, self.ff2_winner
        )
        self.final_score = self.strategy.predict_score(self._winner, self._runner_up)
