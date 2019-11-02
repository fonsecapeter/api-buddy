import json
from bs4 import BeautifulSoup
from colorama import Fore, Style
from requests import Response
from requests.cookies import RequestsCookieJar
from typing import MutableMapping, Optional
from ..utils.formatting import (
    format_dict_like_thing,
    highlight_syntax,
    JSON,
)
from ..utils.typing import Preferences

BINARY_CONTENT_TYPES = [
    'audio',
    'image',
    'video',
    'pdf',
]
TAGS_TO_SKIP = [
    'a',
    'button'
    'footer',
    'head',
    'header',
    'nav',
    'script',
    'style',
]


def _print_response_details(
            headers: MutableMapping[str, str],
            cookies: RequestsCookieJar,
            indent: Optional[int],
            theme: Optional[str],
        ) -> None:
    if headers:
        print(format_dict_like_thing('Headers', headers, indent, theme))
    if cookies:
        print(format_dict_like_thing('Cookies', cookies, indent, theme))
    print()


def _strip_html(content: str) -> str:
    """Parse tags and strip away stuff"""
    soup = BeautifulSoup(content, features='html.parser')
    for section in soup(TAGS_TO_SKIP):
        section.extract()
    raw_text = soup.get_text()
    lines = []
    for line in raw_text.split('\n'):
        if line:
            lines.append(line.strip())
    return '\n'.join(lines)


def format_response(
            resp: Response,
            indent: Optional[int],
            theme: Optional[str],
            print_binaries: bool = False,
        ) -> str:
    content_type = resp.headers.get('content-type', '')
    if JSON in content_type:
        try:
            return highlight_syntax(
                json.dumps(resp.json(), indent=indent),  # reindent
                theme,
            ).rstrip()
        except (ValueError, TypeError):
            pass
    elif 'html' in content_type:
        return _strip_html(resp.text).rstrip()
    if not print_binaries:
        is_binary = any([
            binary_type in content_type
            for binary_type in BINARY_CONTENT_TYPES
        ])
        if is_binary:
            return f'Binary response: {content_type}'
    return resp.text.rstrip()


def print_response(resp: Response, prefs: Preferences) -> None:
    verbose = prefs['verboseness']['response']
    theme = prefs['theme']
    indent = prefs['indent']
    arrow = f'{Fore.BLACK}{Style.BRIGHT}=>'
    if resp.ok:
        status_color = Fore.GREEN
    else:
        status_color = Fore.YELLOW
    if verbose:
        status = (
            f'{status_color}{resp.status_code} '
            f'{Style.NORMAL}{resp.reason}{Style.RESET_ALL}'
        )
    else:
        status = f'{status_color}{resp.status_code}{Style.RESET_ALL}'
    print(f'{arrow} {status}')
    if verbose:
        _print_response_details(resp.headers, resp.cookies, indent, theme)
    print(format_response(
        resp,
        indent,
        theme,
        prefs['verboseness']['print_binaries'],
    ))
