import json
from bs4 import BeautifulSoup
from requests import Response
from requests.cookies import RequestsCookieJar
from typing import MutableMapping
from ..utils.typing import Preferences
from ..utils import format_dict_like_thing

INDENT = 2
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
        ) -> None:
    if headers:
        print(format_dict_like_thing('Headers', headers))
    if cookies:
        print(format_dict_like_thing('Cookies', cookies))
    print('Content:')


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


def format_response(resp: Response) -> str:
    try:
        formatted = json.dumps(resp.json(), indent=INDENT)
    except (json.decoder.JSONDecodeError, TypeError):
        formatted = resp.text
        if '<!DOCTYPE html>' in formatted:
            formatted = _strip_html(formatted)
    return formatted


def print_response(resp: Response, prefs: Preferences) -> None:
    print(f'=> {resp.status_code}')
    if prefs['verboseness']['response'] is True:
        _print_response_details(resp.headers, resp.cookies)
    print(format_response(resp))
