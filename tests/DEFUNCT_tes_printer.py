from _pytest.capture import CaptureFixture
from _pytest.python import Metafunc

from gamewinner.bracket.bracket import Bracket
from gamewinner.printers import Printer, console_printers, file_printers


def pytest_generate_tests(metafunc: Metafunc) -> None:
    console_fixture = "console_printer"
    if console_fixture in metafunc.fixturenames:
        metafunc.parametrize(console_fixture, console_printers, scope="function")

    file_fixture = "file_printer"
    if file_fixture in metafunc.fixturenames:
        metafunc.parametrize(file_fixture, file_printers, scope="function")


class TestPrinters:
    def test_console_print(
        self,
        strategized_bracket: Bracket,
        console_printer: Printer,
        capsys: CaptureFixture,
    ) -> None:
        console_printer.print(strategized_bracket)

        capture = capsys.readouterr()
        assert capture.out and capture.out != "\n"

    def test_file_print(
        self, strategized_bracket: Bracket, file_printer: Printer
    ) -> None:
        file_printer.print(strategized_bracket)
