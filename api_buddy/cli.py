import click
from urllib.parse import urljoin
from .constants import VERSION, PREFS_FILE
from .preferences import load_prefs
from .session.oauth import get_oauth_session


@click.command()
@click.option('--version', is_flag=True, help='Show version and exit.')
def run(version: bool) -> None:
    """Explore the 23andMe API from your terminal

    Check out https://github.com/fonsecapeter/api-buddy for more info
    """
    if version:
        click.echo(VERSION)
        return
    prefs = load_prefs(PREFS_FILE)
    sesh = get_oauth_session(prefs, PREFS_FILE)
    resp = sesh.get(urljoin(prefs['api_url'], '3/account'))
    click.echo(resp.json())


if __name__ == '__main__':
    run()
