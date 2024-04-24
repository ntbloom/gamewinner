from typing import Any

import typer
from rich import print as rprint
from rich.console import Console
from typing_extensions import Annotated

from gamewinner.bracket import available_years, this_year
from gamewinner.bracket.scoring import BracketProvider, Providers, available_providers
from gamewinner.gamewinner import play, rank_brackets
from gamewinner.printers import all_printers
from gamewinner.printers.basic_file_printer import BasicFilePrinter
from gamewinner.printers.iprinter import Printer
from gamewinner.strategies import BestRankWins, Strategy, available_strategies

PRINTERS: dict[str, Printer] = {
    printer.name: printer for printer in all_printers  # type: ignore
}
PROVIDERS: dict[str, BracketProvider] = {
    provider.name: provider for provider in available_providers
}
STRATEGIES: dict[str, Strategy] = {
    strategy.name: strategy for strategy in available_strategies
}
YEARS: dict[int, int] = {year: year for year in available_years}

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
    strategy: str = typer.Option(BestRankWins().name, help="strategy you want to use"),
    year: int = typer.Option(this_year, help="year you want to use"),
    printer: str = typer.Option(BasicFilePrinter.name, help="printer to use"),
    score_all: Annotated[bool, typer.Option("--score_all")] = False,
    provider: str = typer.Option(
        Providers.espn.name, help="which scoring system to use"
    ),
) -> None:
    try:
        _year = YEARS[year]
    except KeyError:
        _error_msg("year", year, YEARS)

    if score_all:
        try:
            _provider = PROVIDERS[provider]
            rank_brackets(_year, _provider)
        except KeyError:
            _error_msg("provider", provider, PROVIDERS)

    else:
        _strategy = STRATEGIES.get(strategy, None)
        if not _strategy:
            _error_msg("strategy", strategy, STRATEGIES)
        _printer = PRINTERS.get(printer, None)
        if not _printer:
            _error_msg("printer", printer, PRINTERS)

        play(_strategy, _year, _printer)  # type: ignore


if __name__ == "__main__":
    app()
