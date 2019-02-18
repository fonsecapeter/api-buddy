import json
from bs4 import BeautifulSoup
from requests import Response

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


def print_response(resp: Response) -> None:
    print(f'=> {resp.status_code}')
    try:
        print(json.dumps(resp.json(), indent=INDENT))
    except json.decoder.JSONDecodeError:
        text = resp.text
        if '<!DOCTYPE html>' in text:
            text = _strip_html(text)
        print(text)
