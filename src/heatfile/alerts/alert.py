from sys import platform

import click
from colorama import Fore, init, Style


if platform == "win":
    init()


class Alert:
    __INFO = "INFO"
    __WARNING = "WARNING"
    __SUCCESS = "SUCCESS"

    @classmethod
    def raise_error_message(cls, message: str) -> None:
        message = f"{Style.BRIGHT + Fore.RED}{message}"
        cls.help_message()
        raise click.ClickException(message)

    @classmethod
    def info_message(cls, message: str, bold: bool = False) -> None:
        click.secho(f"[{cls.__INFO}]: {message}", fg="blue", bold=bold)

    @classmethod
    def warning_message(cls, message: str, bold: bool = False) -> None:
        click.secho(f"[{cls.__WARNING}]: {message}", fg="yellow", bold=bold)

    @classmethod
    def success_message(cls, message: str, bold: bool = False) -> None:
        click.secho(f"[{cls.__SUCCESS}]: {message}", fg="green", bold=bold)

    @classmethod
    def help_message(cls, bold: bool = False) -> None:
        context = click.get_current_context()
        click.secho(
            f"\nType {context.command.name} -H for help.\n", fg="white", bold=bold
        )
