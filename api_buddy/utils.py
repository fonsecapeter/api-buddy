from typing import Optional
from os import path
from urllib.parse import urljoin

VERSION = '0.1.0'
PREFS_FILE = '~/.api-buddy.yml'
ROOT_DIR = path.dirname(path.dirname(__file__))


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
