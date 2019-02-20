import mock
from copy import deepcopy
from requests_oauthlib import OAuth2Session

from api_buddy.session.oauth import get_oauth_session, APPLICATION_JSON
from api_buddy.config.preferences import load_prefs
from ..helpers import (
    FAKE_API_URL,
    FAKE_ACCESS_TOKEN,
    FAKE_STATE,
    TEST_PREFERENCES,
    TEST_OPTIONS,
    TEMP_FILE,
    TempYAMLTestCase,
    explode,
    mock_get,
    mock_post,
)

NEW_ACCESS_TOKEN = 'mint-chip'


class TestGetOauthSession(TempYAMLTestCase):
    @mock_get()
    def test_returns_a_session(self):
        sesh = get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        assert type(sesh) == OAuth2Session

    @mock_get()
    def test_adds_headers(self):
        sesh = get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        headers = sesh.headers
        assert headers['Accept'] == APPLICATION_JSON
        assert headers['Content-Type'] == APPLICATION_JSON

    @mock_get()
    @mock.patch('api_buddy.session.oauth._authenticate')
    def test_skips_authentication_if_token_is_valid(self, mock_authenticate):
        mock_authenticate.side_effect = explode  # should not get called
        sesh = get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        assert sesh.token['access_token'] == FAKE_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')  # within Oauth2.fetch_token
    @mock.patch('webbrowser.open')
    @mock.patch('api_buddy.session.oauth._get_authorization_response_url')
    def test_re_authenticates_if_token_is_expired(self, mock_auth_resp_url, mock_open):
        mock_auth_resp_url.return_value = f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        sesh = get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        assert sesh.token['access_token'] == NEW_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')  # within Oauth2.fetch_token
    @mock.patch('webbrowser.open')
    @mock.patch('api_buddy.session.oauth._get_authorization_response_url')
    def test_writes_new_token_if_re_authenticating(self, mock_auth_resp_url, mock_open):
        mock_auth_resp_url.return_value = f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        prefs = load_prefs(TEMP_FILE)
        assert prefs['access_token'] == NEW_ACCESS_TOKEN
