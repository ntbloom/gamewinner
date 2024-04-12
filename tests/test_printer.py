from _pytest.python import Metafunc

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers import Printer, file_printers


def pytest_generate_tests(metafunc: Metafunc) -> None:
    file_fixture = "file_printer"
    if file_fixture in metafunc.fixturenames:
        metafunc.parametrize(file_fixture, file_printers, scope="function")


class TestPrinters:
    def test_file_print(
        self, strategized_bracket: Bracket, file_printer: Printer
    ) -> None:
        file_printer.print(strategized_bracket)
