"""Explore OAuth2 APIs from your console

Check out https://github.com/fonsecapeter/api-buddy for more info

Usage:
  api-buddy <endpoint>
  api-buddy get <endpoint>
  api-buddy (-h | --help)
  api-buddy (-v | --version)

Options:
  -v, --version  Show installed version
  -h, --help     Show this help message
"""
from .constants import VERSION, PREFS_FILE
from .exceptions import APIBuddyException, exit_with_exception
from .config.preferences import load_prefs
from .config.options import load_options
from .request import send_request
from .response import print_response
from .session.oauth import get_oauth_session


def run() -> None:
    opts = load_options(__doc__)
    if opts['--version']:
        print(VERSION)
        return
    try:
        prefs = load_prefs(PREFS_FILE)
    except APIBuddyException as err:
        exit_with_exception(err)
        return
    sesh = get_oauth_session(prefs, PREFS_FILE)
    resp = send_request(sesh, prefs, opts)
    print_response(resp)


if __name__ == '__main__':
    run()
