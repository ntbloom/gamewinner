import pytest

from gamewinner.bracket.bracket import Bracket
from gamewinner.teams.alternate_names import alternate_names
from gamewinner.teams.team import get_definitive_name


class TestGetDefinitiveName:
    @pytest.mark.parametrize(
        "raw,definitive",
        [
            ("ASU", "Arizona State"),
            ("UConn", "Connecticut"),
            ("Uconn", "Connecticut"),
            ("Yale", "Yale"),
            ("uab", "UAB"),
            ("DUKE", "Duke"),
            ("DuKe", "Duke"),
            ("UCSB", "UC Santa Barbara"),
            ("University of California Santa Barbara", "UC Santa Barbara"),
        ],
    )
    def test_get_definitive_name(self, raw: str, definitive: str) -> None:
        assert get_definitive_name(raw) == definitive

    def test_definitive_name_raises_exception_on_bad_name(self) -> None:
        with pytest.raises(ValueError):
            get_definitive_name("This University Doesn't Exist")

    def test_alternate_names_are_in_alphabetical_order(self) -> None:
        # we can do this since python populates dictionaries in order
        names_unsorted = list(alternate_names.keys())
        assert names_unsorted == sorted(
            names_unsorted
        ), "`alternate_names` entries are not in alphabetical order"

    def test_all_teams_are_in_alternate_names(self, test_year: int) -> None:
        bracket = Bracket(test_year)
        teams = {team for team in bracket.teams.keys()}
        for team in teams:
            assert get_definitive_name(team)
