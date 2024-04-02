import pytest

import tests.expected_first_round as expected_first_round
from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.game import Game
from gamewinner.bracket.parser import Parser
from gamewinner.teams.team import Team


class TestBasicBuild:
    def test_parser(self, test_year: int) -> None:
        parser = Parser(test_year)
        assert parser.west_plays
        assert parser.year == test_year
        for region in (parser.east, parser.west, parser.south, parser.midwest):
            assert len(region) == 16
            assert sum(region.keys()) == 136
            assert len(set(region.values())) == 16
        assert len(set(parser.teams)) == 64
        for team in parser.teams:
            assert isinstance(team, Team)

    def test_bracket_builds(self, test_year: int) -> None:
        bracket = Bracket(test_year)
        assert bracket
        assert len(set(bracket.teams)) == 64

    @pytest.mark.parametrize(
        "year,first_round_games",
        [
            (2024, expected_first_round.FIRST_ROUND2024),
        ],
    )
    def test_first_round_games(self, year: int, first_round_games: set[Game]) -> None:
        bracket = Bracket(year)
        bracket.play()
        assert len(bracket.games) == 63
        assert len(first_round_games) == 32
        assert len(bracket.first_round) == 32
        for game in bracket.first_round:
            teams = {game.team1.name, game.team2.name}
            assert teams in first_round_games


# class TestBracketBestWins:
#     def test_bracket_with_best_wins(self, best_wins_bracket: Bracket) -> None:
#         bracket = best_wins_bracket
#
#         # should be all #1s
#         actual_final_four = {team.name for team in bracket.final_four}
#         expected_final_four = {"Gonzaga", "Baylor", "Arizona", "Kansas"}
#         assert actual_final_four == expected_final_four
#
#         assert bracket.winner.name == "Arizona"
#         assert bracket.runner_up.name == "Gonzaga"
#
#     class TestBracketWorstWins:
#         def test_bracket_with_worst_wins(self, worst_wins_bracket: Bracket) -> None:
#             bracket = worst_wins_bracket
#
#             actual_final_four = {team.name for team in bracket.final_four}
#             expected_final_four = {
#                 "Georgia State",
#                 "Norfolk State",
#                 "Wright State",
#                 "Texas Southern",
#             }
#             assert actual_final_four == expected_final_four
#
#             assert bracket.winner.name == "Texas Southern"
#             assert bracket.runner_up.name == "Georgia State"
#
#     @pytest.mark.parametrize(
#         "matchup",
#         (
#             ("Gonzaga", "Georgia State"),
#             ("Boise State", "Memphis"),
#             ("Connecticut", "New Mexico State"),
#             ("Arkansas", "Vermont"),
#             ("Alabama", "Notre Dame"),
#             ("Texas Tech", "Montana State"),
#             ("Michigan State", "Davidson"),
#             ("Duke", "Cal State Fullerton"),
#         ),
#     )
#     def test_all_first_round_matchups(
#         self, best_wins_bracket: Bracket, matchup: tuple[str, str]
#     ) -> None:
#         assert matchup in best_wins_bracket.games

# @pytest.mark.parametrize("region", GeographicRegion)
# def test_final_four(self, region: GeographicRegion, reference_year: Year) -> None:
#     if region == GeographicRegion.WEST:
#         pytest.skip("West can't play West, skipping matchup")
#
#     # inject the test west_plays variable into the 2022 data
#     year = Year(reference_year.year, west_plays=region)
#
#     bracket = Bracket(year, BestRankWins(), year)
#     bracket.play()
#
#     assert len(bracket.final_four) == 2
#     for game in bracket.final_four:
#         assert len(game) == 2
#
#     match region:
#         case GeographicRegion.EAST:
#             expected = {"Gonzaga", "Baylor"}, {"Arizona", "Kansas"}
#         case GeographicRegion.SOUTH:
#             expected = {"Gonzaga", "Arizona"}, {"Kansas", "Baylor"}
#         case GeographicRegion.MIDWEST:
#             expected = {"Gonzaga", "Kansas"}, {"Baylor", "Arizona"}
#         case _:
#             raise ValueError("unreachable")
#
#     actual = set(team.name for team in bracket.final_four[0]), set(
#         team.name for team in bracket.final_four[1]
#     )
#     for matchup in expected:
#         assert matchup in actual
