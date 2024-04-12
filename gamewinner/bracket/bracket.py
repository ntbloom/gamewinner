from __future__ import annotations

import logging
from dataclasses import dataclass

from gamewinner.bracket.exceptions import BracketLogicError
from gamewinner.bracket.game import Game
from gamewinner.bracket.parser import Parser
from gamewinner.bracket.stage import Stage
from gamewinner.strategies import BestRankWins
from gamewinner.strategies.istrategy import Strategy
from gamewinner.teams.team import Team


@dataclass
class BracketNode:
    round: Stage
    parent: BracketNode | None = None
    left_child: BracketNode | None = None
    right_child: BracketNode | None = None
    team: Team | None = None

    def __repr__(self) -> str:
        return f"{self.round=}, {self.parent=}"


class Bracket:

    def __init__(self, year: int):
        self.__log = logging.getLogger("bracket")
        self.__year = year
        self.__parser = Parser(self.__year)
        self.__root = BracketNode(round=Stage.Winner)
        self.__teams: dict[str, Team] = {}

        # set of all games; maybe we don't need this?
        self.__games: set[Game] = set()

        # get each round
        self.first_round: set[Game] = set()
        self.second_round: set[Game] = set()
        self.sweet_sixteen: set[Game] = set()
        self.elite_eight: set[Game] = set()
        self.final_four: set[Game] = set()
        self.finals: Game | None = None
        self.winner: Team | None = None

        self.__build(self.__root)
        self.__strategy = BestRankWins()

    @property
    def games(self) -> set[Game]:
        return self.__games

    @property
    def teams(self) -> dict[str, Team]:
        return self.__teams

    def play(self, strategy: Strategy = BestRankWins()) -> None:
        self.__strategy = strategy
        self.__strategy.prepare(self.__year, self.__teams)
        self.__play(self.__root)

    def __play(self, node: BracketNode) -> None:
        if not node:
            pass
        assert node, "out of bounds"

        if node.left_child.team and node.right_child.team:
            stage = node.left_child.round
            team1 = node.left_child.team
            team2 = node.right_child.team
            winner = self.__strategy.pick(team1, team2)
            game = Game(team1=team1, team2=team2, predicted_winner=winner, stage=stage)
            self.__games.add(game)
            self.__log.debug(f"{game}->{winner}")
            node.team = winner
            self.__log.debug("moving up")

            match stage:
                case Stage.FirstRound:
                    self.first_round.add(game)

                case Stage.SecondRound:
                    self.second_round.add(game)

                case Stage.SweetSixteen:
                    self.sweet_sixteen.add(game)

                case Stage.EliteEight:
                    self.elite_eight.add(game)

                case Stage.FinalFour:
                    self.final_four.add(game)

                case Stage.Finals:
                    self.__log.debug(f"Play finished: {len(self.__games)} played")
                    self.finals = game
                    self.winner = node.team
                    return

                case _:
                    return self.__play(node.parent)

        if node.left_child.team and not node.right_child.team:
            self.__log.debug("moving right")
            return self.__play(node.right_child)

        if not node.left_child.team and not node.right_child.team:
            self.__log.debug("moving left")
            return self.__play(node.left_child)

        self.__log.debug("moving up")
        return self.__play(node.parent)

    def __build(self, node: BracketNode) -> None:
        assert node, "out of bounds!"
        if node.round < 1:
            raise BracketLogicError
        self.__log.debug(f"{node.round=}")

        if node.round == Stage.FirstRound:
            node.team = self.__parser.teams.pop()
            self.__log.debug(
                f"adding {node.team.region.name} #{node.team.rank} {node.team.name}"
            )
            self.__teams[node.team.name] = node.team
            self.__log.debug("moving up")
            return self.__build(node.parent)

        if node.left_child is None and node.round > Stage.FirstRound:
            node.left_child = BracketNode(round=Stage(node.round - 1), parent=node)
            self.__log.debug("moving left")
            return self.__build(node.left_child)

        if node.right_child is None and node.round > Stage.FirstRound:
            node.right_child = BracketNode(round=Stage(node.round - 1), parent=node)
            self.__log.debug("moving right")
            return self.__build(node.right_child)

        if node.round == Stage.Winner and node.left_child and node.right_child:
            self.__log.debug(f"Build finished: {len(self.__teams)} teams populated")
            return

        self.__log.debug("moving up")
        return self.__build(node.parent)
