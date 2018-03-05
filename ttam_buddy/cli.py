import click
from .constants import VERSION


@click.command()
@click.option('--version', is_flag=True, help='Show version and exit.')
def run(version: bool) -> None:
    """Explore the 23andMe API from your console"""
    if version:
        click.echo(VERSION)
        return
    click.echo(':p')


if __name__ == '__main__':
    run()
