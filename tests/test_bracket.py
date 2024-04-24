import pytest

from gamewinner.bracket.bracket import Bracket
from tests.expected_teams import Expected2023, Expected2024, ExpectedTeamData


class TestBasicBracket:
    def test_bracket_builds_and_plays(self, test_year: int) -> None:
        bracket = Bracket(test_year)
        assert bracket
        assert len(set(bracket.teams)) == 64
        assert not bracket.winner

        bracket.predict()
        assert len(bracket.games) == 63
        assert bracket.winner
        assert len(bracket.final_four) == 2
        assert len(bracket.elite_eight) == 4
        assert len(bracket.sweet_sixteen) == 8
        assert len(bracket.second_round) == 16
        assert len(bracket.first_round) == 32

    @pytest.mark.parametrize(
        "year,expected_data",
        [
            (2023, Expected2023),
            (2024, Expected2024),
        ],
    )
    def test_bracket_play_best_wins(
        self, year: int, expected_data: ExpectedTeamData
    ) -> None:
        bracket = Bracket(year)
        bracket.predict()

        for game in bracket.first_round:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.first_round

        for game in bracket.second_round:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.second_round

        for game in bracket.sweet_sixteen:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.sweet_sixteen

        for game in bracket.elite_eight:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.elite_eight

        for game in bracket.final_four:
            teams = {game.team1.name, game.team2.name}
            assert teams in expected_data.final_four

        assert bracket.finals
        assert {
            bracket.finals.team1.name,
            bracket.finals.team2.name,
        } == expected_data.finals

        assert bracket.winner and bracket.winner.name == expected_data.winner
