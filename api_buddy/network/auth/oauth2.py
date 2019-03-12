import webbrowser
from os import environ
from typing import Optional
from urllib.parse import urljoin
from requests_oauthlib import OAuth2Session

from api_buddy.typing import Preferences, Options
from api_buddy.config.preferences import save_prefs

APPLICATION_JSON = 'application/json'
HEADERS = {
    'Accept': APPLICATION_JSON,
    'Content-Type': APPLICATION_JSON,
}


def _get_authorization_response_url() -> str:
    return input('Enter the full url: ')  # pragma: no cover


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


def get_oauth2_session(
            opts: Options,
            prefs: Preferences,
            prefs_file_name: str,
        ) -> OAuth2Session:
    """Initialize OAuth2 session"""
    sesh = OAuth2Session(
        client_id=prefs['oauth2']['client_id'],
        redirect_uri=prefs['oauth2']['redirect_uri'],
        scope=' '.join(prefs['oauth2']['scopes']),
        token={'access_token': prefs['oauth2']['access_token']},
    )
    sesh.headers.update(HEADERS)
    return sesh


def reauthenticate_oauth2(
            sesh: OAuth2Session,
            prefs: Preferences,
            prefs_file: str,
        ) -> OAuth2Session:
    """Get a new oauth token for an existing session

    Also save it to preferences
    """
    access_token = _authenticate(
        sesh,
        client_secret=prefs['oauth2']['client_secret'],
        api_url=prefs['api_url'],
        redirect_uri=prefs['oauth2']['redirect_uri'],
        state=prefs['oauth2']['state'],
    )
    prefs['oauth2']['access_token'] = access_token
    save_prefs(prefs, prefs_file)
    return sesh