from dataclasses import dataclass

from gamewinner.bracket.exceptions import MatchupError
from gamewinner.bracket.round import Round
from gamewinner.teams.team import Team


@dataclass
class Game:
    team1: Team
    team2: Team
    round: Round

    def __post_init__(self):
        if self.team1 == self.team2:
            raise MatchupError("Same team can't play each other")

        if (self.team1.region == self.team2.region) and (
            self.round == Round.FinalFour or self.round == Round.Finals
        ):
            raise MatchupError("Late rounds must intra-region matchup")

        if (
            self.team1.region != self.team2.region
            and self.round != Round.FinalFour
            and self.round != Round.Finals
            and self.round != Round.Winner
        ):
            raise MatchupError("Early rounds must be inter-region matchup")

    def __eq__(self, other) -> bool:
        return {self.team1, self.team2} == {
            other.team1,
            other.team2,
        } and self.round == other.round

    def __hash__(self) -> int:
        return hash(f"{self.team1.name}{self.team2.name}{self.round}")

    def __repr__(self) -> str:
        return f"{self.round.name}: {self.team1.name}/{self.team2.name}"
