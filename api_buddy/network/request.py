import urllib3
import requests
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
from .session import reauthenticate

DNS = 'http://1.1.1.1'


def _check_interwebs_connection() -> None:
    try:
        requests.get(DNS, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise APIBuddyException(
            title='There was a problem connecting to the internet',
            message='Are you on WiFi?'
        )


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
            sesh: requests.Session,
            prefs: Preferences,
            opts: Options,
            prefs_file: str,
            retry: bool = True,
        ) -> requests.Response:
    """Send the http request, reauthenticating if necessary"""
    _check_interwebs_connection()
    url = api_url_join(
        prefs['api_url'],
        prefs['api_version'],
        opts['<endpoint>'],
    )
    method = opts['<method>']
    params = opts['<params>']
    data = opts['<data>']
    verify = prefs['verify_ssl']
    if prefs['verboseness']['request'] is True:
        print_request(method, url, sesh.headers, params, data)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if method == GET:
        resp = sesh.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
            verify=verify,
        )
    elif method == POST:
        resp = sesh.post(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
            verify=verify,
        )
    elif method == PUT:
        resp = sesh.put(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
            verify=verify,
        )
    elif method == PATCH:
        resp = sesh.patch(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
            verify=verify,
        )
    elif method == DELETE:
        resp = sesh.delete(
            url,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT,
            verify=verify,
        )
    else:
        raise APIBuddyException(
            title='Something went wrong',
            message='Try a different http method'
        )
    if prefs['auth_type'] is not None:
        if retry and resp.status_code == prefs['auth_test_status']:
            sesh = reauthenticate(sesh, prefs, prefs_file)
            resp = send_request(sesh, prefs, opts, prefs_file, retry=False)
    return resp
