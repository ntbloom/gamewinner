from typing import NamedTuple

from gamewinner.team import GeographicRegion


class Year(NamedTuple):
    year: int
    west_plays: GeographicRegion

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Year):
            return NotImplemented
        return self.year == other.year


year2022 = Year(year=2022, west_plays=GeographicRegion.EAST)
year2023 = Year(year=2023, west_plays=GeographicRegion.MIDWEST)

available_years = (year2022, year2023)
this_year = year2023
test_year = year2022
