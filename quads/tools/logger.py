import logging
import sys


class ColorFormatter(logging.Formatter):
    """
    Logging Formatter to add colors and count warning / errors
    """

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    green = "\x1b[32;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_msg = "%(message)s"

    FORMATS = {
        logging.DEBUG: green + format_msg + reset,
        logging.INFO: format_msg,
        logging.WARNING: yellow + format_msg + reset,
        logging.ERROR: red + format_msg + reset,
        logging.CRITICAL: bold_red + format_msg + reset,
    }

    def format(self, record):
        if sys.stdout.isatty():
            log_fmt = self.FORMATS.get(record.levelno)
        else:
            log_fmt = self.format_msg
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
