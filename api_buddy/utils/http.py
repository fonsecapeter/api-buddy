from colorama import Fore, Style
from typing import Dict, List, Union
from .typing import QueryParams
from .exceptions import APIBuddyException

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


def pack_query_params(
            params: List[str]
        ) -> QueryParams:
    """Convert string query params into key-value pairs

    ['key1=val1', 'key2=val2', 'key2=val3']
    => {'key1': 'val1', 'key2': ['val2', 'val3']}
    """
    keyed_params: Dict[str, Union[str, List[str]]] = {}
    for param in params:
        try:
            key, val = param.split('=')
        except ValueError:
            raise APIBuddyException(
                title='One of your query params is borked',
                message=(
                    f'{Fore.MAGENTA}{param}{Style.RESET_ALL} should contain '
                    f'one and only one {Fore.MAGENTA}"="{Style.RESET_ALL}'
                ),
            )
        prev_val = keyed_params.get(key)
        if prev_val is None:
            keyed_params[key] = val
        elif isinstance(prev_val, str):
            keyed_params[key] = [prev_val, val]
        else:
            prev_val.append(val)
    return keyed_params


def unpack_query_params(
            params: QueryParams
        ) -> List[str]:
    """Convert key-value pairs into string query params

    {'key1': 'val1', 'key2': ['val2', 'val3']}
    => ['key1=val1', 'key2=val2', 'key2=val3']
    """
    unpacked: List[str] = []
    for name, value in params.items():
        if isinstance(value, list):
            for item in value:
                unpacked.append(f'{name}={item}')
        else:
            unpacked.append(f'{name}={value}')
    return unpacked
