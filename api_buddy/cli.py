"""Explore OAuth2 APIs from your console with API Buddy

It's as easy as:
api get some-endpoint

HTTP Method defaults to get:
api this-endpoint

You can add query params in key=val format:
api get \\
  my/favorite/endpoint \\
  first_name=cosmo \\
  last_name=kramer

You can also add request body data in JSON format:
api post \\
  some-endpoint \\
  '{"id": 1, "field": "value"}'

Note the single-quotes, you can also expand this accross
multiple lines:
api post \\
  some-endpoint \\
  '{
     "id": 1,
     "field": "value"
  }'

Your preferences live in in ~/.api-buddy.yml
You'll have to specify these (with examples shown):
  api_url: https://base.api.url.com
  client_id: your_client_id
  client_secret: your_client_secret
  scopes: [one_scope, another_scope]

And you can optionally specify these (with defaults shown):
  redirect_uri: http://localhost:8080/
  auth_fail_path: 401
  api_version: null

Arguments:
  http_method  (optional, default: get) One of
                 [get, post, patch, put, delete]
  endpoint     The relative path to an API endpoint
  params       (optional) A list of key=val query params
  data         (optional) A JSON string of request body
                 data, for all methods but 'get'

Usage:
  api get <endpoint> [<params> ...]
  api post <endpoint> [<params> ...] [<data>]
  api patch <endpoint> [<params> ...] [<data>]
  api put <endpoint> [<params> ...] [<data>]
  api delete <endpoint> [<params> ...] [<data>]
  api <endpoint> [<params> ...]
  api (-h | --help)
  api (-v | --version)

Options:
  -h, --help     Show this help message
  -v, --version  Show installed version

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
