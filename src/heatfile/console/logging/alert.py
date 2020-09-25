import logging
from sys import platform

from colorama import Fore, init, Style

logger = logging.getLogger(__name__)


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


class Alert:
    def __init__(self) -> None:
        handler = logging.StreamHandler()
        handler.setFormatter(IOFormatter())
        logger.addHandler(handler)

    def error(self, message: str) -> None:
        logger.error(message)

    def info(self, message: str) -> None:
        logger.setLevel(logging.INFO)
        logger.info(message)

    def warning(self, message: str) -> None:
        logger.warning(message)

    def debug(self, message: str) -> None:
        logger.debug(message)

    def help(self) -> None:
        logger.setLevel(logging.INFO)
        logger.info("Type [COMMAND] -H for help.\n")
