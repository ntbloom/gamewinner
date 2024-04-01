from __future__ import annotations

from dataclasses import dataclass

from gamewinner.bracket.round import Round
from gamewinner.teams.team import Team


@dataclass
class BracketNode:
    round: Round
    parent: BracketNode | None = None
    left_child: BracketNode | None = None
    right_child: BracketNode | None = None
    team: Team | None = None

    built: bool = False


RANKS = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
