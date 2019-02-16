"""Explore OAuth2 APIs from your console

Check out https://github.com/fonsecapeter/api-buddy for more info

Usage:
  api-buddy [options]

Options:
  -v, --version  Show installed version
  -h, --help     Show this help message
"""
import json
from docopt import docopt
from urllib.parse import urljoin
from .constants import VERSION, PREFS_FILE
from .preferences import load_prefs
from .session.oauth import get_oauth_session


def run() -> None:
    opts = docopt(__doc__)
    if opts['--version']:
        print(VERSION)
        return
    prefs = load_prefs(PREFS_FILE)
    sesh = get_oauth_session(prefs, PREFS_FILE)
    resp = sesh.get(urljoin(prefs['api_url'], '3/account'))
    print(json.dumps(resp.json(), indent=2))


if __name__ == '__main__':
    run()
