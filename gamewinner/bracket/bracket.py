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
        self._log = logging.getLogger("bracket")

        self._parser = Parser(year)
        self._root = BracketNode(round=Stage.Winner)

        self.teams: dict[str, Team] = {}
        self.games: set[Game] = set()
        self._first_round: set[Game] = set()
        # self.second_round: set[Game] = set()
        # self.sweet_sixteen: set[Game] = set()
        # self.elite_eight: set[Game] = set()
        # self.final_foud: set[Game] = set()
        # self.finals: set[Game] = set()

        self.__build(self._root)
        self._strategy = BestRankWins()

    @property
    def first_round(self) -> set[Game]:
        return self._first_round

    # @property
    # def games(self) -> set[tuple[str, str]]:
    #     # TODO: sort team names by rank
    #     return self._games
    #
    # @property
    # def final_four(self) -> set[Team]:
    #     raise NotImplementedError
    #
    # @property
    # def runner_up(self) -> Team:
    #     raise NotImplementedError
    #
    # @property
    # def winner(self) -> Team:
    #     raise NotImplementedError
    #
    # @property
    # def root(self) -> BracketNode:
    #     return self._root

    def play(self, strategy: Strategy = BestRankWins()) -> None:
        self._strategy = strategy
        self.__play(self._root)

    def __play(self, node: BracketNode) -> None:
        if not node:
            pass
        assert node, "out of bounds"

        if node.left_child.team and node.right_child.team:
            stage = node.left_child.round
            team1 = node.left_child.team
            team2 = node.right_child.team
            winner = self._strategy.pick(team1, team2)
            game = Game(team1=team1, team2=team2, predicted_winner=winner, stage=stage)
            self.games.add(game)
            self._log.debug(f"{game}->{winner}")
            node.team = winner
            self._log.debug("moving up")

            if stage == Stage.FirstRound:
                self._first_round.add(game)

            if node.round == Stage.Winner and node.team:
                self._log.info(f"Play finished: {len(self.games)} played")
                return

            return self.__play(node.parent)

        if node.left_child.team and not node.right_child.team:
            self._log.debug("moving right")
            return self.__play(node.right_child)

        if not node.left_child.team and not node.right_child.team:
            self._log.debug("moving left")
            return self.__play(node.left_child)

        self._log.debug("moving up")
        return self.__play(node.parent)

    def __build(self, node: BracketNode) -> None:
        assert node, "out of bounds!"
        if node.round < 1:
            raise BracketLogicError
        self._log.debug(f"{node.round=}")

        if node.round == Stage.FirstRound:
            node.team = self._parser.teams.pop()
            self._log.debug(
                f"adding {node.team.region.name} #{node.team.rank} {node.team.name}"
            )
            self.teams[node.team.name] = node.team
            self._log.debug("moving up")
            return self.__build(node.parent)

        if node.left_child is None and node.round > Stage.FirstRound:
            node.left_child = BracketNode(round=Stage(node.round - 1), parent=node)
            self._log.debug("moving left")
            return self.__build(node.left_child)

        if node.right_child is None and node.round > Stage.FirstRound:
            node.right_child = BracketNode(round=Stage(node.round - 1), parent=node)
            self._log.debug("moving right")
            return self.__build(node.right_child)

        if node.round == Stage.Winner and node.left_child and node.right_child:
            self._log.info(f"Build finished: {len(self.teams)} teams populated")
            return

        self._log.debug("moving up")
        return self.__build(node.parent)
