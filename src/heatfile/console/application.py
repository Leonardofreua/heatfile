from os import getcwd
from pathlib import Path
from typing import Optional, Union

import click
from click_help_colors import HelpColorsGroup

from heatfile.__version__ import __version__
from heatfile.alerts import Alert
from .commands.tree import Tree


@click.group(cls=HelpColorsGroup, help_headers_color="green", help_options_color="blue")
@click.version_option(version=__version__, help="Display current version")
@click.help_option("--help", "-H", help="Display list of commands and informations")
def cli() -> None:
    pass


@cli.command(help="Display in Tree structure")
@click.help_option("--help", "-H", help="Display list of commands and informations")
@click.option(
    "--path",
    "-P",
    type=click.Path(),
    default=getcwd(),
    show_default=True,
    help="Directory path",
)
@click.option(
    "--search",
    "-S",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Search string",
)
def tree(path, search):  # type: (Path, Union[Optional[str], None]) -> None
    if Path(path).is_file() and search is None:
        Alert.raise_error_message(
            "Provide a string to find references in the given file."
        )
    elif not Path(path).exists():
        Alert.raise_error_message("Directory/File not found.")

    Tree.build_tree(Path(path), search)
