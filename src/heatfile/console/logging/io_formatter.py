import logging
from sys import platform

from colorama import Fore, init, Style

if platform == "win":
    init()


class IOFormatter(logging.Formatter):
    _colors = {
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "debug": Fore.CYAN,
        "info": Fore.WHITE,
    }

    def format(self, record):
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.msg

            if level in self._colors:
                msg = f"{Style.BRIGHT + self._colors[level]}{msg}"

            return msg

        return super(IOFormatter, self).format(record)
