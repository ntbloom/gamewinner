import logging
from abc import ABC, abstractmethod

from gamewinner.team import Team


class IStrategy(ABC):
    _log = logging.getLogger(__name__)

    def prepare(self, teams: dict[str, Team]) -> None:
        """
        Called before any games are played, including the first four. This can
        be used to add datapoints to any teams or further amend the strategy
        after the brackets have been laid out.

        It is not necessary to overload this method; the default is a no-op.
        """
        pass

    def adjust(self, teams: dict[str, Team]) -> None:
        """
        Called before each round, including in between the first four and the
        first round.  This can be used to amend strategies based on the results
        of previous games.

        It is not necessary to overload this method; the default is a no-op.
        """
        pass

    @abstractmethod
    def pick(self, team1: Team, team2: Team) -> tuple[Team, Team]:
        """Pick a game winner"""
        return NotImplemented

    @abstractmethod
    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        """Predict the score of a game"""
        return NotImplemented


Strategy = IStrategy
