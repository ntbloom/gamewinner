from typing import NamedTuple

from gamewinner.bracket.geographic_region import GeographicRegion


class Year(NamedTuple):
    year: int
    west_plays: GeographicRegion

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Year):
            return NotImplemented
        return self.year == other.year


year2022 = Year(year=2022, west_plays=GeographicRegion.EAST)
year2023 = Year(year=2023, west_plays=GeographicRegion.MIDWEST)
year2024 = Year(year=2024, west_plays=GeographicRegion.EAST)

available_years = (year2022, year2023, year2024)
this_year = year2024
# if this_year == year2024:
#     from rich.console import Console
#
#     console = Console()
#     console.print(
#         "[red bold]WARNING: using preliminary data before first four, results are trash!!!",  # noqa
#         style="red",
#     )
