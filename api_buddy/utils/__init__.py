from requests.cookies import RequestsCookieJar
from typing import Any, Dict, MutableMapping, Optional, Union
from os import path
from urllib.parse import urljoin

VERSION = '0.1.0'
PREFS_FILE = '~/.api-buddy.yml'
ROOT_DIR = path.dirname(path.dirname(path.dirname(__file__)))
MAX_LINE_LENGTH = 50
INDENT = '  '
VARIABLE_CHARS = '#{}'


class UtilException(Exception):
    """Just like APIBuddyException but no need to circular import"""
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message


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


def flat_str_dict(
            thing_name: str,
            thing: Dict[Any, Any],
            check_special_chars: bool = False,
        ) -> Dict[str, str]:
    """Convert dictionary like thing into strict, flat Dict[str, str]"""
    processed_vars = {}
    for name, val in thing.items():
        if isinstance(val, (dict, list)):
            raise UtilException(
                title=f'Your "{name}" {thing_name} is not gonna fly',
                message='It can\'t be nested, try something simpler',
            )
        # bool capitalization is unpredictable
        if isinstance(val, bool):
            raise UtilException(
                title=f'Your "{name}" {thing_name} is a boolean',
                message=(
                    'You\'re going to have to throw some quotes around that '
                    'bad boy so I know how to capitalize it. Something like\n'
                    f'  {name}: \'{str(val).lower()}\''
                ),
            )
        if isinstance(name, bool):
            display_name = str(name).lower()
            raise UtilException(
                title=(
                    f'Yo, you have a boolean for a {thing_name} name "{name}"'
                ),
                message=(
                    'Rename it or throw some quotes around that bad boy so I '
                    'know how to capitalize it. Something like:\n'
                    f'  \'{display_name}\': {val}'
                ),
            )
        if name is None:
            raise UtilException(
                title='You must use a sting name',
                message='Using null or None as a name is not a thing.',
            )
        if check_special_chars:
            any_name_has_special_chars = any(
                special_char in str(name) for special_char in VARIABLE_CHARS
            )
            if any_name_has_special_chars:
                raise UtilException(
                    title=f'Your {thing_name} name "{name}" is too funky',
                    message=(
                        f'You can\'t use any of these special characters:\n  '
                        ' '.join([f'"{c}"' for c in tuple(VARIABLE_CHARS)])
                    ),
                )
        processed_vars[str(name)] = str(val)
    return processed_vars
