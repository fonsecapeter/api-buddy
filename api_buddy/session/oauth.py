import webbrowser
import requests
from os import environ
from typing import Optional
from urllib.parse import urljoin
from requests_oauthlib import OAuth2Session

from ..exceptions import APIBuddyException
from ..typing import Preferences, Options
from ..utils import REQUEST_TIMEOUT
from ..config.preferences import save_prefs

DNS = 'http://1.1.1.1'
APPLICATION_JSON = 'application/json'
HEADERS = {
    'Accept': APPLICATION_JSON,
    'Content-Type': APPLICATION_JSON,
}


def _get_authorization_response_url() -> str:
    return input('Enter the full url: ')  # pragma: no cover


def _check_interwebs_connection() -> None:
    try:
        requests.get(DNS, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise APIBuddyException(
            title='There was a problem connecting to the internet',
            message='Are you on WiFi?'
        )


def _authenticate(
            sesh: OAuth2Session,
            client_secret: str,
            api_url: str,
            redirect_uri: str,
            state: Optional[str] = None,
        ) -> str:
    """Perform OAuth2 Flow and get a new token

    Note:
        Implicitly updates the OAuth2Session
    """
    authorization_url, state = sesh.authorization_url(
        urljoin(api_url, 'authorize'),
        state=state,
        kwargs={'select_profile': 'true'},
    )
    print(
        f'Opening browser to visit:\n\n{authorization_url}\n\n'
        'Sign in and go through the DSA, then copy the url.\n'
    )
    webbrowser.open(authorization_url)
    authorization_response = _get_authorization_response_url()
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # allow non-http redirect_uri
    token = sesh.fetch_token(
        urljoin(api_url, 'token'),
        authorization_response=authorization_response,
        client_secret=client_secret,
        include_client_id=True,
    )
    return str(token['access_token'])


def get_oauth_session(
            opts: Options,
            prefs: Preferences,
            prefs_file_name: str,
        ) -> OAuth2Session:
    """Initialize OAuth2 session"""
    _check_interwebs_connection()
    sesh = OAuth2Session(
        client_id=prefs['client_id'],
        redirect_uri=prefs['redirect_uri'],
        scope=' '.join(prefs['scopes']),
        token={'access_token': prefs['access_token']},
    )
    sesh.headers.update(HEADERS)
    return sesh


def reauthenticate(
            sesh: OAuth2Session,
            prefs: Preferences,
            prefs_file: str,
        ) -> OAuth2Session:
    """Get a new oauth token for an existing session

    Also save it to preferences
    """
    access_token = _authenticate(
        sesh,
        client_secret=prefs['client_secret'],
        api_url=prefs['api_url'],
        redirect_uri=prefs['redirect_uri'],
        state=prefs['state'],
    )
    prefs['access_token'] = access_token
    save_prefs(prefs, prefs_file)
    return sesh
