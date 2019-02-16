import webbrowser
from os import environ
from typing import Optional
from urllib.parse import urljoin
from requests_oauthlib import OAuth2Session

from ..typing import Preferences
from ..config.preferences import save_prefs

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


def get_oauth_session(prefs: Preferences, prefs_file_name: str) -> OAuth2Session:
    """Initialize OAuth2 session, reauthorizing if needed

    Notes:
        - Saves new token to preferences if re-authenticating
    """
    sesh = OAuth2Session(
        client_id=prefs['client_id'],
        redirect_uri=prefs['redirect_uri'],
        scope=' '.join(prefs['scopes']),
        token={'access_token': prefs['access_token']},
    )
    resp = sesh.get(urljoin(prefs['api_url'], prefs['auth_test_path']))
    if resp.status_code == prefs['auth_test_status']:
        access_token = _authenticate(
            sesh,
            client_secret=prefs['client_secret'],
            api_url=prefs['api_url'],
            redirect_uri=prefs['redirect_uri'],
            state=prefs['state'],
        )
        prefs['access_token'] = access_token
        save_prefs(prefs, prefs_file_name)
    sesh.headers.update(HEADERS)
    return sesh
