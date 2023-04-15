from enum import unique, Enum


@unique
class GeographicRegion(Enum):
    WEST = "West"
    EAST = "East"
    SOUTH = "South"
    MIDWEST = "Midwest"
