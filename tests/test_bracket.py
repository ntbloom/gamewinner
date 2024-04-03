import pytest

import tests.expected_teams as expected_teams
from gamewinner.bracket.bracket import Bracket
from gamewinner.bracket.game import Game
from gamewinner.bracket.parser import Parser
from gamewinner.teams.team import Team, get_definitive_name


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


class TestBracketPlayBestWins:
    @pytest.mark.parametrize(
        "year,first_round_games",
        [
            (2024, expected_teams.FIRST_ROUND2024),
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

    @pytest.mark.parametrize(
        "year,elite_eight",
        [
            (2024, expected_teams.ELITE_EIGHT2024),
        ],
    )
    def test_elite_eight(self, year: int, elite_eight: set[set[str]]) -> None:
        bracket = Bracket(year)
        bracket.play()
        assert len(bracket.elite_eight) == 4
        for game in bracket.elite_eight:
            teams = {game.team1.name, game.team2.name}
            assert teams in elite_eight

    @pytest.mark.parametrize(
        "year,final_four",
        [
            (2024, expected_teams.FINAL_FOUR2024),
        ],
    )
    def test_final_four(self, year: int, final_four: set[set[str]]) -> None:
        bracket = Bracket(year)
        bracket.play()
        assert len(bracket.final_four) == 2
        for game in bracket.final_four:
            teams = {game.team1.name, game.team2.name}
            assert teams in final_four

    @pytest.mark.parametrize(
        "year,finals",
        [
            (2024, expected_teams.FINALS2024),
        ],
    )
    def test_finals(self, year: int, finals: set[str]) -> None:
        bracket = Bracket(year)
        bracket.play()
        assert {bracket.finals.team1.name, bracket.finals.team2.name} == finals

    @pytest.mark.parametrize(
        "year,predicted_winner",
        [
            (2024, "UConn"),
        ],
    )
    def test_winner(self, year: int, predicted_winner: str) -> None:
        bracket = Bracket(year)
        bracket.play()
        assert bracket.winner.name == get_definitive_name(predicted_winner)
