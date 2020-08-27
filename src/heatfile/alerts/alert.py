import click


class Alert:
    __INFO = "INFO"
    __ERROR = "ERROR"
    __WARNING = "WARNING"
    __SUCCESS = "SUCCESS"

    @classmethod
    def info_message(cls, message, bold=False):
        click.secho(f"[{cls.__INFO}]: {message}", fg="blue", bold=bold)

    @classmethod
    def error_message(cls, message):
        click.secho(f"[{cls.__ERROR}]: {message}", fg="red", bold=True)

    @classmethod
    def warning_message(cls, message, bold=False):
        click.secho(f"[{cls.__WARNING}]: {message}", fg="yellow", bold=bold)

    @classmethod
    def success_message(cls, message, bold=False):
        click.secho(f"[{cls.__SUCCESS}]: {message}", fg="green", bold=bold)

    @classmethod
    def help_message(cls, bold=False):
        context = click.get_current_context()
        click.secho(
            f"\nType {context.command.name} -H for help.", fg="white", bold=bold
        )
