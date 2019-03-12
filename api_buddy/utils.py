from requests.cookies import RequestsCookieJar
from typing import Any, Dict, MutableMapping, Optional, Union
from os import path
from urllib.parse import urljoin

VERSION = '0.1.0'
PREFS_FILE = '~/.api-buddy.yml'
ROOT_DIR = path.dirname(path.dirname(__file__))
REQUEST_TIMEOUT = 5  # seconds
GET = 'get'
POST = 'post'
PATCH = 'patch'
PUT = 'put'
DELETE = 'delete'
HTTP_METHODS = (
    GET,
    POST,
    PATCH,
    PUT,
    DELETE,
)
MAX_LINE_LENGTH = 50
INDENT = '  '
OAUTH2 = 'oauth2'
AUTH_TYPES = (
    OAUTH2,
)


def api_url_join(
            api_url: str,
            api_version: Optional[str],
            endpoint: str,
        ) -> str:
    """Joins base api url with api version and endpoint

        - a, None, c => a/c
        - a, b, c => a/b/c
    """
    path = endpoint.lstrip('/')
    if api_version is not None:
        path = f'{api_version}/{path}'
    return urljoin(api_url, path)


def format_dict_like_thing(
            name: str,
            thing: Union[
                Dict[str, Any],
                MutableMapping[str, str],
                RequestsCookieJar,
            ]
        ) -> str:
    """Format dictionaries for nice printing"""
    formatted = f'{name}:'
    for key, val in thing.items():
        display_val = val
        if isinstance(val, list):
            display_val = f'\n{INDENT}{INDENT}- '.join(val)
            display_val = f'\n{INDENT}{INDENT}- {display_val}'
        formatted += f'\n{INDENT}{key}: {display_val}'
    return formatted
