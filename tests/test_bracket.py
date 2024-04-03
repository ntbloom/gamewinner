import pytest

from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.parser import Parser
from gamewinner.teams.team import Team
from tests.expected_teams import Expected2024, ExpectedTeamData


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

    def test_bracket_builds_and_plays(self, test_year: int) -> None:
        bracket = Bracket(test_year)
        assert bracket
        assert len(set(bracket.teams)) == 64

        bracket.play()
        assert len(bracket.games) == 63
        assert bracket.winner
        assert len(bracket.final_four) == 2
        assert len(bracket.elite_eight) == 4
        # assert len(bracket.sweet_sixteen) == 8
        # assert len(bracket.second_round) == 16
        assert len(bracket.first_round) == 32


@pytest.mark.parametrize("year,expected_data", [(2024, Expected2024)])
class TestBracketPlayBestWins:
    def test_first_round_games(
        self, year: int, expected_data: ExpectedTeamData
    ) -> None:
        bracket = Bracket(year)
        bracket.play()

        assert bracket.winner.name == expected_data.winner

        assert {
            bracket.finals.team1.name,
            bracket.finals.team2.name,
        } == expected_data.finals

        for game in bracket.final_four:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.final_four

        for game in bracket.elite_eight:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.elite_eight

        for game in bracket.sweet_sixteen:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.sweet_sixteen

        for game in bracket.second_round:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.second_round

        for game in bracket.first_round:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.first_round
