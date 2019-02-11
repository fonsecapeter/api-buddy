import webbrowser
from os import environ
from typing import Iterable, Optional
from urllib.parse import urljoin
from requests_oauthlib import OAuth2Session


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
        f'Opening browser to visit:\n\n{authorization_url}\n'
        'Sign in and go through the DSA, then copy the url.\n'
    )
    webbrowser.open(authorization_url)
    authorization_response = _get_authorization_response_url()
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # allow non-http redirect_uri
    token = sesh.fetch_token(
        urljoin(api_url, 'token'),
        authorization_response=authorization_response,
        client_secret=client_secret,
    )
    return str(token['access_token'])


def get_oauth_session(
            client_id: str,
            client_secret: str,
            scopes: Iterable[str],
            api_url: str,
            redirect_uri: str,
            state: Optional[str],
            access_token: str,
            auth_test_path: str,  # endpoint to test if token is expired
            auth_fail_status: int = 401,  # status code if expired
        ) -> OAuth2Session:
    """Initialize OAuth2 session, reauthorizing if needed"""
    sesh = OAuth2Session(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=' '.join(scopes),
        token={'access_token': access_token},
    )
    resp = sesh.get(urljoin(api_url, auth_test_path))
    if resp.status_code == auth_fail_status:
        access_token = _authenticate(
            sesh,
            client_secret=client_secret,
            api_url=api_url,
            redirect_uri=redirect_uri,
            state=state,
        )
        print(f'access_token: {access_token}')
    return sesh
