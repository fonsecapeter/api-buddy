from colorama import Fore, Style
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.data import JsonLexer, YamlLexer
from pygments.styles import get_style_by_name
from requests.cookies import RequestsCookieJar
from typing import Any, cast, Dict, List, MutableMapping, Optional, Union
from urllib.parse import urljoin
from .exceptions import APIBuddyException
from ..config.themes import SHELLECTRIC, Shellectric

VARIABLE_CHARS = '#{}'
JSON = 'json'
YAML = 'yaml'


def format_yaml_line(name: str, val: str) -> str:
    return (
        f'  {Fore.YELLOW}{name}{Fore.BLACK}{Style.BRIGHT}:'
        f' {Fore.RED}{val}{Style.RESET_ALL}'
    )


def format_yaml_list(things: List[str]) -> str:
    delim = f'\n  {Fore.BLACK}{Style.BRIGHT}- {Fore.RED}'
    formatted_things = delim.join(sorted(things))
    return f'{delim}{formatted_things}{Style.RESET_ALL}'


def highlight_syntax(
            stuff: str,
            theme: Optional[str],
            lang: str = JSON
        ) -> str:
    """Colorize stuff with syntax highlighting"""
    if lang == JSON:
        lexer = JsonLexer()
    else:
        lexer = YamlLexer()
    if theme is None:
        return stuff
    elif theme == SHELLECTRIC:
        pygment_theme = Shellectric
    else:  # theme already validated in preferences loading
        pygment_theme = get_style_by_name(theme)
    return cast(str, highlight(
        stuff,
        lexer,
        Terminal256Formatter(style=pygment_theme),
    ))


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
            ],
            theme: Optional[str] = None,
        ) -> str:
    """Format dictionaries for nice printing"""
    delim = f'\n    - '
    formatted = f'{name}:'
    for key, val in thing.items():
        display_val = val
        if isinstance(val, list):
            display_val = delim.join(val)
            display_val = f'{delim}{display_val}'
        key_val_pair = f'\n  {key}: {display_val}'
        formatted += key_val_pair
    if theme is not None:
        formatted = highlight_syntax(formatted, theme, lang=YAML)
    return formatted.rstrip()


def flat_str_dict(
            thing_name: str,
            thing: Dict[Any, Any],
            check_special_chars: bool = False,
        ) -> Dict[str, str]:
    """Convert dictionary like thing into strict, flat Dict[str, str]"""
    processed_vars = {}
    for name, val in thing.items():
        if isinstance(val, (dict, list)):
            raise APIBuddyException(
                title=(
                    f'Your {Fore.MAGENTA}{Style.BRIGHT}"{name}" '
                    f'{Style.NORMAL}{thing_name}{Style.RESET_ALL} '
                    'is not gonna fly'
                ),
                message='It can\'t be nested, try something simpler',
            )
        # bool capitalization is unpredictable
        if isinstance(val, bool):
            display_val = f'\'{str(val).lower()}\''
            raise APIBuddyException(
                title=(
                    f'Your {Fore.MAGENTA}{Style.BRIGHT}"{name}" '
                    f'{Style.NORMAL}{thing_name}{Style.RESET_ALL} is a boolean'
                ),
                message=(
                    'You\'re going to have to throw some quotes around that '
                    'bad boy so I know how to capitalize it. Something like:\n'
                    f'  {format_yaml_line(name, display_val)}'
                ),
            )
        if isinstance(name, bool):
            display_name = f'\'{str(name).lower()}\''
            raise APIBuddyException(
                title=(
                    f'Yo, you have a boolean for a {thing_name} name "{name}"'
                ),
                message=(
                    'Rename it or throw some quotes around that bad boy so I '
                    'know how to capitalize it. Something like:\n'
                    f'  {format_yaml_line(display_name, val)}'
                ),
            )
        if name is None:
            raise APIBuddyException(
                title='You must use a string name',
                message=(
                    f'Using {Fore.MAGENTA}{Style.BRIGHT}null{Style.RESET_ALL} '
                    f'or {Fore.MAGENTA}{Style.BRIGHT}None{Style.RESET_ALL} as '
                    'a name is not a thing.'
                ),
            )
        if check_special_chars:
            any_name_has_special_chars = any(
                special_char in str(name) for special_char in VARIABLE_CHARS
            )
            if any_name_has_special_chars:
                display_special_chars = (
                    ' '.join([f'"{c}"' for c in tuple(VARIABLE_CHARS)])
                )
                raise APIBuddyException(
                    title=f'Your {thing_name} name "{name}" is too funky',
                    message=(
                        f'You can\'t use any of these special characters:\n  '
                        f'{Fore.MAGENTA}{Style.BRIGHT}{display_special_chars}'
                        f'{Style.RESET_ALL}'
                    ),
                )
        processed_vars[str(name)] = str(val)
    return processed_vars
