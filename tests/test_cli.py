import pytest
from typer.testing import CliRunner

from cli import app
from gamewinner.strategies import BestRankWins
from gamewinner.years import this_year

VALUE_ERROR_EXIT_CODE = 1


@pytest.fixture(scope="function")
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope="class")
def valid_strategy() -> str:
    return BestRankWins().name


@pytest.fixture(scope="class")
def valid_year() -> str:
    return str(this_year.year)


class TestCli:
    @pytest.mark.parametrize("year", [2022, 2023])
    def test_years_work(
        self, cli_runner: CliRunner, year: int, valid_strategy: str
    ) -> None:
        assert (
            cli_runner.invoke(
                app, ["--year", str(year), "--strategy", valid_strategy]
            ).exit_code
            == 0
        )

    def test_skipping_years_is_cool(
        self, cli_runner: CliRunner, valid_strategy: str
    ) -> None:
        assert cli_runner.invoke(app, ["--strategy", valid_strategy]).exit_code == 0

    def test_catch_bad_strategy(self, cli_runner: CliRunner, valid_year: str) -> None:
        assert (
            cli_runner.invoke(
                app, ["--year", valid_year, "--strategy", "not_a_real_strategy"]
            ).exit_code
            == VALUE_ERROR_EXIT_CODE
        )

    def test_catch_bad_years(self, cli_runner: CliRunner, valid_strategy: str) -> None:
        assert (
            cli_runner.invoke(
                app, ["--year", "1999", "--strategy", valid_strategy]
            ).exit_code
            == VALUE_ERROR_EXIT_CODE
        )
