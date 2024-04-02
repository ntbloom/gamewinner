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

    def __repr__(self) -> str:
        return f"{self.round=}, {self.parent=}"
