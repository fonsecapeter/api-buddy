import json
from bs4 import BeautifulSoup
from colorama import Fore, Style
from requests import Response
from requests.cookies import RequestsCookieJar
from typing import MutableMapping, Optional
from ..utils.formatting import format_dict_like_thing, highlight_syntax
from ..utils.typing import Preferences

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
            theme: Optional[str],
        ) -> None:
    if headers:
        print(format_dict_like_thing('Headers', headers, theme))
    if cookies:
        print(format_dict_like_thing('Cookies', cookies, theme))
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
        ) -> str:
    try:
        formatted = highlight_syntax(
            json.dumps(resp.json(), indent=indent),
            theme,
        )
    except (json.decoder.JSONDecodeError, TypeError):
        formatted = resp.text
        if '<!DOCTYPE html>' in formatted:
            formatted = _strip_html(formatted)
    return formatted.rstrip()


def print_response(resp: Response, prefs: Preferences) -> None:
    verbose = prefs['verboseness']['response']
    theme = prefs['theme']
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
        _print_response_details(resp.headers, resp.cookies, theme)
    print(format_response(resp, prefs['indent'], theme))
