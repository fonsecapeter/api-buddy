from requests import Response, Session
from urllib.parse import urljoin
from .typing import Preferences, Options


def send_request(sesh: Session, prefs: Preferences, opts: Options) -> Response:
    if opts['get']:
        resp = sesh.get(urljoin(prefs['api_url'], opts['<endpoint>']))
    return resp
