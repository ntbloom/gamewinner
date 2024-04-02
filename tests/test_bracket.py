import pytest

from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.parser import Parser
from gamewinner.strategies.istrategy import Strategy
from gamewinner.teams.team import Team


@pytest.mark.parametrize("year", (2024,))
class TestBasicBuild:
    def test_parser(self, year: int) -> None:
        parser = Parser(year)
        assert parser.west_plays
        assert year
        for region in (parser.east, parser.west, parser.south, parser.midwest):
            assert len(region) == 16
            assert sum(region.keys()) == 136
            assert len(set(region.values())) == 16
        assert len(set(parser.teams)) == 64
        for team in parser.teams:
            assert isinstance(team, Team)

    def test_bracket_builds(self, best_wins: Strategy, year: int) -> None:
        bracket = Bracket(best_wins, year)
        assert bracket


first_round_2024 = {
    ("UNC", "Wagner"),
    ("Mississippi State", "Michigan State"),
    ("Saint Mary's", "Grand Canyon"),
    ("Alabama", "Charleston"),
    ("Clemson", "New Mexico"),
    ("Baylor", "Colgate"),
    ("Dayton", "Nevada"),
    ("Arizona", "Long Beach State"),
    ("Purdue", "Grambling"),
    ("Utah State", "TCU"),
    ("Gonzaga", "McNeese"),
    ("Kansas", "Samford"),
    ("South Carolina", "Oregon"),
    ("Creighton", "Akron"),
    ("Texas", "Colorado State"),
    ("Tennessee", "Saint Peter's"),
    ("UConn", "Stetson"),
    ("FAU", "Northwestern"),
    ("San Diego State", "UAB"),
    ("Auburn", "Yale"),
    ("BYU", "Duquesne"),
    ("Illinois", "Morehead State"),
    ("Washington State", "Drake"),
    ("Iowa State", "South Dakota State"),
    ("Houston", "Longwood"),
    ("Nebraska", "Texas A&M"),
    ("Wisconsin", "JMU"),
    ("Duke", "Vermont"),
    ("Texas Tech", "NC State"),
    ("Kentucky", "Oakland"),
    ("Florida", "Colorado"),
    ("Marquette", "Western Kentucky"),
}


@pytest.mark.parametrize(
    "year,first_round_games",
    [
        (2024, first_round_2024),
    ],
)
def test_first_round_games(
    best_wins: Strategy, year: int, first_round_games: set[tuple[str, str]]
) -> None:
    bracket = Bracket(best_wins, year)
    assert len(first_round_games) == 32
    for matchup in first_round_games:
        assert matchup in bracket.games


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
