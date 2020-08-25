from pathlib import Path

import click

from . import __version__
from .tree import Tree


@click.group()
@click.version_option(version=__version__, help="Display current version")
@click.help_option("--help", "-H", help="Display list of commands and informations")
def cli() -> None:
    pass


@cli.command(help="Display in Tree structure")
@click.option("--path", "-P", type=click.Path(), help="Directory path")
@click.option("--search", "-S", type=click.STRING, help="Search string")
def tree(path: Path, search: str) -> None:
    Tree.build_tree(path, search)


def run() -> None:
    cli()
