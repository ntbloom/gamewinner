from __future__ import annotations

import logging

from gamewinner.bracket.bracket_node import BracketNode
from gamewinner.bracket.exceptions import BracketLogicError
from gamewinner.bracket.game import Game
from gamewinner.bracket.parser import Parser
from gamewinner.bracket.stage import Stage
from gamewinner.strategies import BestRankWins
from gamewinner.strategies.istrategy import Strategy
from gamewinner.teams.team import Team


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


#
# class Bracket:
#     def __init__(
#         self,
#         west: RegionalBracket,
#         east: RegionalBracket,
#         south: RegionalBracket,
#         midwest: RegionalBracket,
#         strategy: Strategy,
#         year: Year = this_year,
#     ):
#         self.played = False
#
#         self.west = west
#         self.east = east
#         self.south = south
#         self.midwest = midwest
#
#         self.year = year
#         self._west_machup = year.west_plays
#
#         self._teams = {
#             team.name: team
#             for team in (
#                 self.west.teams
#                 + self.east.teams
#                 + self.south.teams
#                 + self.midwest.teams
#             )
#         }
#         self._region_names = tuple(region.value.lower() for region in GeographicRegion) # noqa
#         self.regions = (self.west, self.east, self.south, self.midwest)
#
#         self.strategy = strategy
#         self.upsets: list[str] = []
#         self._winner: Team | None = None
#         self._runner_up: Team | None = None
#
#     @property
#     def teams(self) -> dict[str, Team]:
#         return self._teams
#
#     @property
#     def final_four(self) -> tuple[tuple[Team, Team], ...]:
#         return tuple(self._final_four)
#
#     @property
#     def runner_up(self) -> Team:
#         if not self._runner_up:
#             raise BracketLogicError("must call `play()` first, or logic is broken")
#         return self._runner_up
#
#     @property
#     def winner(self) -> Team:
#         if not self._winner:
#             raise BracketLogicError("must call `play()` first, or logic is broken")
#         return self._winner
#
#     @staticmethod
#     def create(strategy: Strategy, year: Year) -> Bracket:
#         teamfile = (
#             Path(__file__)
#             .parent.parent.parent.joinpath("data")
#             .joinpath(f"{year.year}.csv")
#         )
#         assert teamfile.exists(), f"Missing teamfile for year {year.year}: {teamfile=}" # noqa
#
#         west_teams: list[Team] = []
#         east_teams: list[Team] = []
#         south_teams: list[Team] = []
#         midwest_teams: list[Team] = []
#         playoffs: list[Team] = []
#         teams: dict[str, Team] = {}
#
#         with open(teamfile, "r") as f:
#             reader = csv.reader(f)
#             reader.__next__()
#             for row in reader:
#                 try:
#                     name, region, rank, wins, losses = row
#                 except ValueError:
#                     raise InvalidDataFile(f"Bad entry for {row}")
#                 match region:
#                     case _ if "Playoff" in region:
#                         _region = region.split("-")[0]
#                         in_playoff = True
#                     case _:
#                         _region = region
#                         in_playoff = False
#                 geographic_region = GeographicRegion(str(_region))
#                 team = Team(
#                     name=name,
#                     region=geographic_region,
#                     rank=int(rank),
#                     wins=int(wins),
#                     losses=int(losses),
#                 )
#                 teams[name] = team
#                 if in_playoff:
#                     playoffs.append(team)
#                 else:
#                     eval(f"{geographic_region.value.lower()}_teams.append(team)")
#
#         # do any adjustments to the strategy now that we know who all the teams are
#         strategy.prepare(teams)
#
#         west = RegionalBracket(GeographicRegion.WEST, west_teams, strategy)
#         east = RegionalBracket(GeographicRegion.EAST, east_teams, strategy)
#         south = RegionalBracket(GeographicRegion.SOUTH, south_teams, strategy)
#         midwest = RegionalBracket(GeographicRegion.MIDWEST, midwest_teams, strategy)
#
#         return Bracket(west, east, south, midwest, strategy, year)
#
#     def play(self) -> None:
#         self.__play_first_round()
#         self.__play_second_round()
#         self.__play_sweet_sixteen()
#         self.__play_elite_eight()
#         self.__play_final_four()
#         self.__play_final()
#         self.played = True
#         for region in self.regions:
#             for upset in region.upsets:
#                 self.upsets.append(upset)
#
#     def __play_round(self, round_name: str) -> None:
#         for reg in self._region_names:
#             cmd = f"self.{reg}.{round_name}()"
#             eval(cmd)
#
#     def __play_first_round(self) -> None:
#         self.__play_round("first_round")
#
#     def __play_second_round(self) -> None:
#         self.__play_round("second_round")
#
#     def __play_sweet_sixteen(self) -> None:
#         self.__play_round("sweet_sixteen")
#
#     def __play_elite_eight(self) -> None:
#         self.__play_round("elite_eight")
#
#     def __play_final_four(self) -> None:
#         # decide the matchups based on who the west bracket is matched against
#         matchups = {
#             "east": self.east.winner,
#             "south": self.south.winner,
#             "midwest": self.midwest.winner,
#         }
#         west_opponent = matchups.pop(self._west_machup.name.lower())
#         self.ff1_winner, self.ff1_loser = self.strategy.pick(
#             self.west.winner, west_opponent
#         )
#         self.ff2_winner, self.ff2_loser = self.strategy.pick(
#             matchups.popitem()[1], matchups.popitem()[1]
#         )
#         self._final_four = (self.ff1_winner, self.ff1_loser), (
#             self.ff2_winner,
#             self.ff2_loser,
#         )
#
#     def __play_final(self) -> None:
#         self._winner, self._runner_up = self.strategy.pick(
#             self.ff1_winner, self.ff2_winner
#         )
#         self.final_score = self.strategy.predict_score(self._winner, self._runner_up)
