from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class MrFreeze(IEvanMiyaStrategy):
    """
    Cool party!  Is Arnold invited?
    """

    @property
    def name(self) -> str:
        return "MrFreeze"

    def _team_metric(self, team: Team) -> float:
        """Get things started by subtracting all the values"""
        total = 0.0

        attributes = self.em_teams[team.name]

        # chill out! get the number really low
        for attribute in attributes:
            total -= attribute

        magic_numbers = [
            238,  # box office receipts for Batman & Robin, in $M
            160,  # film budget, upper end, in $M
            125,  # film budget, low end, in $M
            525,  # Arnold's max bench press in pounds, allegedly
        ]

        # a freeze is coming: magnify the coldness intensity
        total *= magic_numbers.pop(0)

        # it's a cold town: punish teams who don't play on the road
        total += attributes.home_rank * magic_numbers.pop(0)

        # you're not sending me to the cooler: reward teams with a deep bench
        total -= attributes.roster_rank * magic_numbers.pop(0)

        # it doesn't work on the cold-blooded: reward teams not bothered by injury
        total -= attributes.injury_rank * magic_numbers.pop(0)

        # let 's kick some ice!
        return total
