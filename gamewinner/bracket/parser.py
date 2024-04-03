from pathlib import Path

import yaml

from gamewinner.bracket.exceptions import BracketLogicError
from gamewinner.bracket.geographic_region import GeographicRegion
from gamewinner.teams.team import Team

RANKS = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]


class Parser:
    east: dict[int, str] = {}
    west: dict[int, str] = {}
    south: dict[int, str] = {}
    midwest: dict[int, str] = {}

    west_plays: GeographicRegion
    year: int

    teams: list[Team] = []

    def __init__(self, year: int):
        datadir = Path(__file__).parent.parent.parent.joinpath("data")
        assert datadir.exists()
        with open(datadir.joinpath(f"{year}.yaml"), "r") as f:
            data = yaml.safe_load(f)
            self.east = data["East"]
            self.west = data["West"]
            self.south = data["South"]
            self.midwest = data["Midwest"]
            self.west_plays = data["WestPlays"]
            self.year = data["Year"]

            # Make an array of all teams arranged by region and by rank order.
            # We can pop teams out one by one in each region to build the 4
            # quadrants of the bracket. Order only matters in groups of 2, ie:
            # if West plays East, the order doesn't matter as long as West and
            # East are adjacent and South and Midwest are adjacent. This
            # ensures that the winner of the West regional plays the winner of
            # the `WestPlays`
            match self.west_plays:
                case "East":
                    order = ["West", "East", "South", "Midwest"]
                case "South":
                    order = ["West", "South", "East", "Midwest"]
                case "MidWest":
                    order = ["West", "Midwest", "South", "East"]
                case _:
                    raise BracketLogicError("West can't play itself")

            for reg_str in order:
                region: dict[int, str] = eval(f"self.{reg_str.lower()}")
                for rank in RANKS:
                    team = Team(
                        name=region.get(rank),
                        rank=rank,
                        region=GeographicRegion(reg_str),
                    )
                    self.teams.append(team)
