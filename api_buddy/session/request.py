from requests import Response, Session
from ..utils import (
    GET,
    POST,
    PUT,
    PATCH,
    DELETE,
    REQUEST_TIMEOUT,
    api_url_join,
)
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
    method = opts['<method>']
    if method == GET:
        resp = sesh.get(
            url,
            params=opts['<params>'],
            timeout=REQUEST_TIMEOUT,
        )
    elif method == POST:
        resp = sesh.post(
            url,
            params=opts['<params>'],
            data=opts['<data>'],
            timeout=REQUEST_TIMEOUT,
        )
    elif method == PUT:
        resp = sesh.put(
            url,
            params=opts['<params>'],
            data=opts['<data>'],
            timeout=REQUEST_TIMEOUT,
        )
    elif method == PATCH:
        resp = sesh.patch(
            url,
            params=opts['<params>'],
            data=opts['<data>'],
            timeout=REQUEST_TIMEOUT,
        )
    elif method == DELETE:
        resp = sesh.delete(
            url,
            params=opts['<params>'],
            data=opts['<data>'],
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
