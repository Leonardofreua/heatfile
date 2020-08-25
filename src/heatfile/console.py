from pathlib import Path

import click

from . import __version__
from .tree import Tree


class HeatFile:
    # TODO: Remove
    TEST_DIR = ""  # noqa:B950
    TEST_STRING = ""

    def start(self) -> None:
        Tree.build_tree(Path(self.TEST_DIR), self.TEST_STRING)


@click.command()
@click.version_option(version=__version__)
def start() -> None:
    heatFile = HeatFile()
    heatFile.start()
