import requests
import urllib3
from colorama import Fore, Style
from typing import Any, Dict, List, Optional, Union, cast
from yaspin import yaspin

from .session import reauthenticate
from ..utils.exceptions import (
    APIBuddyException,
    ConnectionException,
    TimeoutException,
)
from ..utils.formatting import (
    api_url_join,
    format_dict_like_thing,
    format_json_with_title,
)
from ..utils.http import (
    GET,
    POST,
    PUT,
    PATCH,
    DELETE,
)
from ..utils.spin import spin
from ..utils.typing import Preferences, Options


def _send_request(
            sesh: requests.Session,
            method: str,
            url: str,
            params: Dict[str, Union[str, List[str]]],
            data: Any,
            verify: bool,
            timeout: int,
        ) -> requests.Response:
    with yaspin(spin):
        if method == GET:
            return (sesh.get(
                url,
                params=params,
                timeout=timeout,
                verify=verify,
            ))
        elif method == POST:
            return (sesh.post(
                url,
                params=params,
                json=data,
                timeout=timeout,
                verify=verify,
            ))
        elif method == PUT:
            return (sesh.put(
                url,
                params=params,
                json=data,
                timeout=timeout,
                verify=verify,
            ))
        elif method == PATCH:
            return (sesh.patch(
                url,
                params=params,
                json=data,
                timeout=timeout,
                verify=verify,
            ))
        elif method == DELETE:
            return (sesh.delete(
                url,
                params=params,
                json=data,
                timeout=timeout,
                verify=verify,
            ))
        else:
            raise APIBuddyException(
                title='Something went wrong',
                message='Try a different http method'
            )


def print_request(
            sesh: requests.Session,
            method: str,
            url: str,
            params: Dict[str, Union[str, List[str]]],
            data: Dict[str, Any],
            indent: Optional[int],
            theme: Optional[str],
        ) -> None:
    if hasattr(sesh, '_client'):  # pragma: no cover
        # Add auth info if available
        url, headers, data = sesh._client.add_token(
            url,
            http_method=method,
            body=data,
            headers=sesh.headers,
        )
    else:
        headers = sesh.headers
    print(
        f'\n{Fore.GREEN}{Style.BRIGHT}{method.upper()} '
        f'{Fore.BLUE}{url}{Style.RESET_ALL}'
    )
    if headers:
        print(format_dict_like_thing('Headers', headers, indent, theme))
    if params:
        print(format_dict_like_thing('Query Params', params, indent, theme))
    if data is not None:
        print(format_json_with_title('Data', data, indent, theme))
    print()


def send_request(
            sesh: requests.Session,
            prefs: Preferences,
            opts: Options,
            prefs_file: str,
            retry: bool = True,
        ) -> requests.Response:
    """Send the http request, reauthenticating if necessary"""
    timeout = prefs['timeout']
    url = api_url_join(
        prefs['api_url'],
        prefs['api_version'],
        cast(str, opts['<endpoint>']),
    )
    method = opts['<method>']
    params = opts['<params>']
    data = opts['<data>']
    if prefs['verboseness']['request'] is True:
        print_request(
            sesh,
            cast(str, method),
            url,
            params,
            data,
            prefs['indent'],
            prefs['theme'],
        )
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        resp = _send_request(
            sesh,
            cast(str, method),
            url,
            params,
            data,
            prefs['verify_ssl'],
            timeout,
        )
    except requests.exceptions.ConnectionError:
        raise ConnectionException()
    except requests.exceptions.ReadTimeout:
        raise TimeoutException(timeout)
    except KeyboardInterrupt:
        exit(130)
    if prefs['auth_type'] is not None:
        if retry and resp.status_code == prefs['auth_test_status']:
            sesh = reauthenticate(sesh, prefs, prefs_file)
            resp = send_request(sesh, prefs, opts, prefs_file, retry=False)
    return resp
