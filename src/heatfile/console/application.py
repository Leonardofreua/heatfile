from pathlib import Path

import click

from heatfile.__version__ import __version__
from heatfile.tree import Tree


@click.group()
@click.version_option(version=__version__, help="Display current version")
@click.help_option("--help", "-H", help="Display list of commands and informations")
def cli() -> None:
    pass


@cli.command(help="Display in Tree structure")
@click.help_option("--help", "-H", help="Display list of commands and informations")
@click.option("--path", "-P", type=click.Path(), help="Directory path")
@click.option("--search", "-S", type=click.STRING, help="Search string")
def tree(path: Path, search: str) -> None:
    try:
        Tree.build_tree(path, search)
    except Exception:
        if path is None and not search:
            print("Error: None of the avaible options have been specified.")
            print("Type tree -H for help")
        elif not Path(path).is_dir():
            print("Error: The path should be a directory")
