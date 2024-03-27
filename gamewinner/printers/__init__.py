from gamewinner.printers.basic_file_printer import BasicFilePrinter
from gamewinner.printers.iprinter import Printer  # noqa
from gamewinner.printers.plain_text import PlainText
from gamewinner.printers.with_colors import WithColors

available_printers = (PlainText, WithColors, BasicFilePrinter)
