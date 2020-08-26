import click


def print_help():
    context = click.get_current_context()
    click.echo(context.get_help())
    context.exit()
