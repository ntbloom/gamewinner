from typing import Any

import typer
from rich import print as rprint
from rich.console import Console

from gamewinner import play
from gamewinner.bracket.years import Year, available_years, this_year
from gamewinner.printers import Printer, WithColors, available_printers
from gamewinner.strategies import Strategy, available_strategies

PRINTERS: dict[str, Printer] = {printer.name: printer for printer in available_printers}
STRATEGIES: dict[str, Strategy] = {
    strategy.name: strategy for strategy in available_strategies
}
YEARS: dict[int, Year] = {year.year: year for year in available_years}

app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
)
console = Console()


def _error_msg(tag: str, name: Any, legals: dict[Any, Any]) -> None:
    rprint(
        f"\n[red]Invalid {tag} [bold]`{name}`[/bold]. Must be one of [green]{list(legals.keys())}\n"  # noqa
    )
    raise ValueError(f"illegal {tag}")


@app.command()
def main(
    strategy: str = typer.Option(..., help="strategy you want to use"),
    year: int = typer.Option(this_year.year, help="year you want to use"),
    printer: str = typer.Option(WithColors.name, help="printer to use"),
) -> None:
    _year = YEARS.get(year, None)
    if not _year:
        _error_msg("year", year, YEARS)
    _strategy = STRATEGIES.get(strategy, None)
    if not _strategy:
        _error_msg("strategy", strategy, STRATEGIES)
    _printer = PRINTERS.get(printer, None)
    if not _printer:
        _error_msg("printer", printer, PRINTERS)

    play(_strategy, _year, _printer)  # type: ignore


if __name__ == "__main__":
    app()
