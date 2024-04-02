from pathlib import Path

import yaml

from gamewinner.bracket.geographic_region import GeographicRegion
from gamewinner.teams.team import Team


class Parser:
    east: dict[int, Team] = {}
    west: dict[int, Team] = {}
    south: dict[int, Team] = {}
    midwest: dict[int, Team] = {}

    west_plays: GeographicRegion
    year: int

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
