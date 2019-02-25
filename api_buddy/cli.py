"""Explore OAuth2 APIs from your console

HTTP Method defaults to get
api get-this-endpoint

Query Params should be in key=val format, ex:
api get \
  my/favorite/endpoint \
  first_name=cosmo \
  last_name=kramer

You can edit your preferences in ~/.api-buddy.yml
You'll have to specify these (with examples shown):
  api_url: https://base.api.url.com
    # (str) The base api url you'll be using
  client_id: your_client_id
    # (str) Part of your api provider dev account
  client_secret: your_client_secret
    # (str) Part of your api provider dev account
    #       (PROTECT THIS, IT'S SECRET) 🙊
  scopes: [one_scope, another_scope]
    # (List[str]) Specify which resources you want to
    #             access

You can optionally specify these (with defaults shown):
  redirect_uri: http://localhost:8080/
    # (str) Part of your api provider dev account, needs to
    #       be on localhost
  auth_fail_path: 401
    # (int) Response status code that means you need to
    #       re-authorize
  api_version: 1
    # (Any) If your api uses versioning, you can specify
    #       this and not have to type it all the time.
    #       https://an.api.com/<version>/my-fav-endpoint

Usage:
  api get <endpoint> [<params> ...]
  api post <endpoint> [<params> ...]
  api patch <endpoint> [<params> ...]
  api put <endpoint> [<params> ...]
  api delete <endpoint> [<params> ...]
  api <endpoint> [<params> ...]
  api (-h | --help)
  api (-v | --version)

Options:
  -v, --version  Show installed version
  -h, --help     Show this help message

Check out GitHub for more info
https://github.com/fonsecapeter/api-buddy
"""
from .utils import VERSION, PREFS_FILE
from .exceptions import APIBuddyException, exit_with_exception
from .config.preferences import load_prefs
from .config.options import load_options
from .session.oauth import get_oauth_session
from .session.request import send_request
from .session.response import format_response


def run() -> None:
    try:
        opts = load_options(__doc__)
        if opts['--version']:
            print(VERSION)
            return
        prefs = load_prefs(PREFS_FILE)
        sesh = get_oauth_session(opts, prefs, PREFS_FILE)
        resp = send_request(sesh, prefs, opts, PREFS_FILE)
        print(f'=> {resp.status_code}')
        print(format_response(resp))
    except APIBuddyException as err:
        exit_with_exception(err)
        return


if __name__ == '__main__':
    run()
