from requests import Response, Session
from ..utils import api_url_join, REQUEST_TIMEOUT
from ..typing import Preferences, Options
from ..exceptions import APIBuddyException
from ..session.oauth import reauthenticate


def send_request(
            sesh: Session,
            prefs: Preferences,
            opts: Options,
            prefs_file: str,
            retry: bool = True,
        ) -> Response:
    """Send the http request, reauthenticating if necessary"""
    url = api_url_join(
        prefs['api_url'],
        prefs['api_version'],
        opts['<endpoint>'],
    )
    if opts['get']:
        resp = sesh.get(
            url,
            params=opts['<params>'],
            timeout=REQUEST_TIMEOUT,
        )
    else:
        raise APIBuddyException(
            title='Something went wrong',
            message='Try a different http method'
        )
    if retry and resp.status_code == prefs['auth_test_status']:
        sesh = reauthenticate(sesh, prefs, prefs_file)
        resp = send_request(sesh, prefs, opts, prefs_file, retry=False)
    return resp
