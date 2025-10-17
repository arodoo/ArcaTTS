"""
TTS Module CLI - Entry point.
"""
import click

from .commands import parse, process_work, process, test


@click.group()
def cli():
    """TTS audio generation tool."""
    pass


cli.add_command(parse)
cli.add_command(process_work)
cli.add_command(process)
cli.add_command(test)


if __name__ == '__main__':
    cli()
