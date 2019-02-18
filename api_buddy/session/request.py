from requests import Response, Session
from urllib.parse import urljoin
from ..typing import Preferences, Options
from ..exceptions import APIBuddyException


def send_request(sesh: Session, prefs: Preferences, opts: Options) -> Response:
    url = urljoin(prefs['api_url'], opts['<endpoint>'])
    if opts['get']:
        return sesh.get(url)
    else:
        raise APIBuddyException(
            title='Something went wrong',
            message='Try a different http method'
        )
