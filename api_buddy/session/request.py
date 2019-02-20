from requests import Response, Session
from ..utils import api_url_join
from ..typing import Preferences, Options
from ..exceptions import APIBuddyException


def send_request(
            sesh: Session,
            prefs: Preferences,
            opts: Options
        ) -> Response:
    url = api_url_join(
        prefs['api_url'],
        prefs['api_version'],
        opts['<endpoint>'],
    )
    if opts['get']:
        return sesh.get(url, params=opts['<params>'])
    else:
        raise APIBuddyException(
            title='Something went wrong',
            message='Try a different http method'
        )
