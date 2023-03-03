from __future__ import annotations

from abc import ABC, abstractmethod

from gamewinner.team import Team


class IStrategy(ABC):
    @abstractmethod
    def pick(self, team1: Team, team2: Team) -> Team:
        """Pick a game winner"""
        return NotImplemented

    @abstractmethod
    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        """Predict the score of a game"""
        return NotImplemented


Strategy = IStrategy
