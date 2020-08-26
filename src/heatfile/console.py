from pathlib import Path

import click

from . import __version__
from .tree import Tree
from .utils import click_utils


@click.group()
@click.version_option(version=__version__, help="Display current version")
@click.help_option("--help", "-H", help="Display list of commands and informations")
def cli() -> None:
    pass


@cli.command(help="Display in Tree structure")
@click.option("--path", "-P", type=click.Path(), help="Directory path")
@click.option("--search", "-S", type=click.STRING, help="Search string")
@click.help_option("--help", "-H", help="Display list of commands and informations")
def tree(path: Path, search: str) -> None:
    if path is None or not search:
        click_utils.print_help()

    Tree.build_tree(path, search)


def run() -> None:
    cli()
