import mock
from copy import deepcopy
from requests_oauthlib import OAuth2Session
from unittest import TestCase

from ttam_buddy.session.oauth import get_oauth_session
from ttam_buddy.preferences import Preferences, load_prefs

from ..test_preferences import TEMP_FILE, clean_temp_yml_file
from ..helpers import explode, mock_get, mock_post

FAKE_API_URL = 'https://fake.api.com'
FAKE_ACCESS_TOKEN = 'banana'
NEW_ACCESS_TOKEN = 'mint-chip'
FAKE_STATE = 'california'
TEST_PREFERENCES: Preferences = {
    'api_url': FAKE_API_URL,
    'client_id': 'client_id',
    'client_secret': 'client_secret',
    'scopes': ('a_scope', 'another_scope'),
    'redirect_uri': 'http://localhost:8080/',
    'access_token': FAKE_ACCESS_TOKEN,
    'auth_test_path': 'endpoint',
    'auth_test_status': 401,
    'state': FAKE_STATE,
}


class TestGetOauthSession(TestCase):
    def setUp(self):
        clean_temp_yml_file()

    def tearDown(self):
        clean_temp_yml_file()

    @mock_get()
    def test_returns_a_session(self):
        sesh = get_oauth_session(deepcopy(TEST_PREFERENCES), TEMP_FILE)
        assert type(sesh) == OAuth2Session

    @mock_get()
    @mock.patch('ttam_buddy.session.oauth._authenticate')
    def test_skips_authentication_if_token_is_valid(self, mock_authenticate):
        mock_authenticate.side_effect = explode  # should not get called
        sesh = get_oauth_session(deepcopy(TEST_PREFERENCES), TEMP_FILE)
        assert sesh.token['access_token'] == FAKE_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')  # within Oauth2.fetch_token
    @mock.patch('webbrowser.open')
    @mock.patch('ttam_buddy.session.oauth._get_authorization_response_url')
    def test_re_authenticates_if_token_is_expired(self, mock_auth_resp_url, mock_open):
        mock_auth_resp_url.return_value = f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        sesh = get_oauth_session(deepcopy(TEST_PREFERENCES), TEMP_FILE)
        assert sesh.token['access_token'] == NEW_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')  # within Oauth2.fetch_token
    @mock.patch('webbrowser.open')
    @mock.patch('ttam_buddy.session.oauth._get_authorization_response_url')
    def test_writes_new_token_if_re_authenticating(self, mock_auth_resp_url, mock_open):
        mock_auth_resp_url.return_value = f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        get_oauth_session(deepcopy(TEST_PREFERENCES), TEMP_FILE)
        prefs = load_prefs(TEMP_FILE)
        assert prefs['access_token'] == NEW_ACCESS_TOKEN
