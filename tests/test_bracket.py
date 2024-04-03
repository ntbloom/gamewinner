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
