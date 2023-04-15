from enum import Enum, unique


@unique
class GeographicRegion(Enum):
    WEST = "West"
    EAST = "East"
    SOUTH = "South"
    MIDWEST = "Midwest"
