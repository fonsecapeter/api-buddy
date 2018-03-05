import click
from .constants import VERSION, PREFS_FILE
from .preferences import load_prefs


@click.command()
@click.option('--version', is_flag=True, help='Show version and exit.')
def run(version: bool) -> None:
    """Explore the 23andMe API from your terminal

    Check out https://github.com/fonsecapeter/ttam-buddy for more info
    """
    if version:
        click.echo(VERSION)
        return
    load_prefs(PREFS_FILE)
    click.echo(':p')


if __name__ == '__main__':
    run()
