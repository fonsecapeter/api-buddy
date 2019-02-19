"""Explore OAuth2 APIs from your console

You can edit your preferences in ~/.api-buddy.yml:
  api_url: https://base.api.url.com
  client_id: your_client_id
  client_secret: your_client_secret
  scopes:
    - one_scope
    - another_scope
  redirect_uri: http://localhost:8080/
  auth_test_path: /endpoint_that_requires_token
  auth_fail_path: 401

These last 2 are used to determine if you need a new token
Check out https://github.com/fonsecapeter/api-buddy for more info

Query Params should be in key=val format, ex:
$ api get my/favorite/endpoint first_name=cosmo last_name=kramer

Usage:
  api <endpoint> [<params>...]
  api get <endpoint> [<params>...]
  api (-h | --help)
  api (-v | --version)

Options:
  -v, --version  Show installed version
  -h, --help     Show this help message
"""
from .constants import VERSION, PREFS_FILE
from .exceptions import APIBuddyException, exit_with_exception
from .config.preferences import load_prefs
from .config.options import load_options
from .session.oauth import get_oauth_session
from .session.request import send_request
from .session.response import format_response


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
    print(f'=> {resp.status_code}')
    print(format_response(resp))


if __name__ == '__main__':
    run()
