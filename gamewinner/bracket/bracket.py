from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import no_type_check

from gamewinner.bracket.exceptions import BracketLogicError
from gamewinner.bracket.game import Game
from gamewinner.bracket.parsers import ResultsParser, SeedParser
from gamewinner.bracket.scoring import BracketProvider
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
        self.__seed_parser = SeedParser(self.__year)
        self.__results_parser = (
            ResultsParser(self.__year) if self.__seed_parser.complete else None
        )

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

        self.__build(self.__root)  # type: ignore
        self.__strategy: Strategy = BestRankWins()

        self.__scored = False

    @property
    def games(self) -> set[Game]:
        return self.__games

    @property
    def teams(self) -> dict[str, Team]:
        return self.__teams

    @property
    def year(self) -> int:
        return self.__year

    @property
    def strategy(self) -> str:
        return self.__strategy.name

    def predict(self, strategy: Strategy = BestRankWins()) -> None:
        self.__strategy = strategy
        self.__strategy.prepare(self.__year, self.__teams)
        self.__predict(self.__root)  # type: ignore
        if self.__results_parser:
            self.__scored = True

    def score(self, provider: BracketProvider) -> int:
        assert self.__scored
        points = 0
        for game in self.__games:
            assert (
                game.prediction_correct is not None
            ), "game should have been predicted"
            if game.prediction_correct:
                points += provider.stage_points(game.stage)
        return points

    @no_type_check
    def __predict(self, node: BracketNode) -> None:
        """Make predictions for all 63 games"""
        assert node, "out of bounds"

        if node.left_child.team and node.right_child.team:
            stage = node.left_child.round
            team1 = node.left_child.team
            team2 = node.right_child.team
            winner = self.__strategy.pick(team1, team2)

            if self.__results_parser:
                match stage:
                    case Stage.FirstRound:
                        correct = (
                            winner.name in self.__results_parser.first_round_winners
                        )
                    case Stage.SecondRound:
                        correct = (
                            winner.name in self.__results_parser.second_round_winners
                        )
                    case Stage.SweetSixteen:
                        correct = (
                            winner.name in self.__results_parser.sweet_sixteen_winners
                        )
                    case Stage.EliteEight:
                        correct = (
                            winner.name in self.__results_parser.elite_eight_winners
                        )
                    case Stage.FinalFour:
                        correct = (
                            winner.name in self.__results_parser.final_four_winners
                        )
                    case Stage.Finals:
                        correct = winner.name in self.__results_parser.winner
                    case _:
                        raise Exception("illegal stage")

            else:
                correct = None
            game = Game(
                team1=team1,
                team2=team2,
                predicted_winner=winner,
                stage=stage,
                prediction_correct=correct,
            )
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
                    return self.__predict(node.parent)

        if node.left_child.team and not node.right_child.team:
            self.__log.debug("moving right")
            return self.__predict(node.right_child)

        if not node.left_child.team and not node.right_child.team:
            self.__log.debug("moving left")
            return self.__predict(node.left_child)

        self.__log.debug("moving up")
        return self.__predict(node.parent)

    @no_type_check
    def __build(self, node: BracketNode) -> None:
        """Build the bracket with all first round games staged"""
        assert node, "out of bounds!"
        if node.round < 1:
            raise BracketLogicError
        self.__log.debug(f"{node.round=}")

        if node.round == Stage.FirstRound:
            node.team = self.__seed_parser.teams.pop()
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
