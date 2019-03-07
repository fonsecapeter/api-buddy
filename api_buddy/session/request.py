from requests import Response, Session
from typing import Any, Dict, List, MutableMapping, Union

from ..utils import (
    GET,
    POST,
    PUT,
    PATCH,
    DELETE,
    REQUEST_TIMEOUT,
    api_url_join,
    format_dict_like_thing,
)
from ..typing import Preferences, Options
from ..exceptions import APIBuddyException
from ..session.oauth import reauthenticate


def print_request(
            method: str,
            url: str,
            headers: MutableMapping[str, str],
            params: Dict[str, Union[str, List[str]]],
            data: Dict[str, Any],
        ) -> None:
    print(
        f'{method.upper()} {url}'
    )
    if headers:
        print(format_dict_like_thing('Headers', headers))
    if params:
        print(format_dict_like_thing('Query Params', params))
    if data is not None:
        print(format_dict_like_thing('Data', data))
    print()


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
    params = opts['<params>']
    data = opts['<data>']
    if prefs['verboseness']['request'] is True:
        print_request(method, url, sesh.headers, params, data)
    if method == GET:
        resp = sesh.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    elif method == POST:
        resp = sesh.post(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
        )
    elif method == PUT:
        resp = sesh.put(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
        )
    elif method == PATCH:
        resp = sesh.patch(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
        )
    elif method == DELETE:
        resp = sesh.delete(
            url,
            params=params,
            data=data,
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
