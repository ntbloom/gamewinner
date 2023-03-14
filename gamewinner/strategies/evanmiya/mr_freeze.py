from typing import no_type_check

from gamewinner.strategies.evanmiya.ievanmiya import IEvanMiyaStrategy
from gamewinner.team import Team


class MrFreeze(IEvanMiyaStrategy):
    """
    Cool party!  Is Arnold invited?
    """

    @property
    def name(self) -> str:
        return "MrFreeze"

    @no_type_check
    def _team_metric(self, team: Team) -> float:
        """Get things started by subtracting all the values"""
        total = 0.0

        # chill out! get the number really low
        for attribute in (prop for prop in dir(team) if "evanmiya" in prop):
            total -= eval(f"team.{attribute}")

        magic_numbers = [
            238,  # box office receipts for Batman & Robin, in $M
            160,  # film budget, upper end, in $M
            125,  # film budget, low end, in $M
            525,  # Arnold's max bench press in pounds, allegedly
        ]

        # a freeze is coming: magnify the coldness intensity
        total *= magic_numbers.pop(0)

        # it's a cold town: punish teams who don't play on the road
        total += team.evanmiyaHomeRank * magic_numbers.pop(0)

        # you're not sending me to the cooler: reward teams with a deep bench
        total -= team.evanmiyaRosterRank * magic_numbers.pop(0)

        # it doesn't work on the cold-blooded: reward teams not bothered by injury
        total -= team.evanmiyaInjuryRank * magic_numbers.pop(0)

        # let 's kick some ice!
        return total
