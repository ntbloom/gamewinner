import logging
from abc import ABC, abstractmethod

from gamewinner.teams.team import Team


class IStrategy(ABC):
    _log = logging.getLogger(__name__)

    @property
    def name(self) -> str:
        raise NotImplementedError

    def prepare(self, year: int, teams: dict[str, Team]) -> None:
        """
        Called before any bracket are played, including the first four. This can
        be used to add datapoints to any teams or further amend the strategy
        after the brackets have been laid out.

        It is not necessary to overload this method; the default is a no-op.
        """
        pass

    @abstractmethod
    def pick(self, team1: Team, team2: Team) -> Team:
        """Pick a game winner"""
        raise NotImplementedError

    @abstractmethod
    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        """Predict the score of a game"""
        raise NotImplementedError


Strategy = IStrategy
