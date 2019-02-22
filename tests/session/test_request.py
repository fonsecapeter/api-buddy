from copy import deepcopy
from mock import MagicMock, PropertyMock, patch
from typing import Dict, List, Union

from api_buddy.config.preferences import load_prefs
from api_buddy.exceptions import APIBuddyException
from api_buddy.session.oauth import get_oauth_session
from api_buddy.session.request import send_request
from ..helpers import (
    FAKE_ACCESS_TOKEN,
    FAKE_API_URL,
    FAKE_API_VERSION,
    FAKE_ENDPOINT,
    FAKE_STATE,
    TEST_PREFERENCES,
    TEST_OPTIONS,
    TEMP_FILE,
    explode,
    mock_get,
    mock_post,
    mock_get_side_effect,
    TempYAMLTestCase,
)

NEW_ACCESS_TOKEN = 'mint-chip'


def _mock_param_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {},
            timeout: int = 0,
        ):
    mock_resp = MagicMock()
    type(mock_resp).params = PropertyMock(return_value=params)
    return mock_resp


def _mock_url_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {},
            timeout: int = 0,
        ):
    mock_resp = MagicMock()
    type(mock_resp).url = PropertyMock(return_value=url)
    return mock_resp


class TestSendRequest(TempYAMLTestCase):
    @mock_get()
    @patch('requests.get')
    def test_returns_a_resopnse(self, mock_get):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        mock_resp = send_request(sesh, prefs, opts, TEMP_FILE)
        assert mock_resp.status_code == 200

    @mock_get()
    @patch('requests.get')
    def test_checks_method(self, mock_get):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        opts['get'] = False
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        try:
            send_request(sesh, prefs, opts, TEMP_FILE)
        except APIBuddyException as err:
            assert 'went wrong' in err.title
            assert 'http method' in err.message
        else:
            assert False

    @patch('requests.get')
    @mock_get_side_effect(_mock_url_catcher)
    def test_adds_endpoint_to_api_url(self, mock_get):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        mock_resp = send_request(sesh, prefs, opts, TEMP_FILE)
        assert mock_resp.url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}'

    @patch('requests.get')
    @mock_get_side_effect(_mock_param_catcher)
    def test_uses_params(self, mock_get):
        params = {'fake_param': 'fake_value'}
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        opts['<params>'] = params
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        mock_resp = send_request(sesh, prefs, opts, TEMP_FILE)
        assert mock_resp.params == params

    @patch('requests.get')
    @mock_get_side_effect(_mock_url_catcher)
    def test_uses_api_version_if_given(self, mock_get):
        params = {'fake_param': 'fake_value'}
        prefs = deepcopy(TEST_PREFERENCES)
        prefs['api_version'] = FAKE_API_VERSION
        opts = deepcopy(TEST_OPTIONS)
        opts['<params>'] = params
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        mock_resp = send_request(sesh, prefs, opts, TEMP_FILE)
        assert mock_resp.url == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}'

    @mock_get()
    @patch('requests.get')
    @patch('api_buddy.session.oauth._authenticate')
    def test_skips_authentication_if_token_is_valid(self, mock_authenticate, mock_get):
        mock_authenticate.side_effect = explode()  # should not get called
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        send_request(sesh, prefs, opts, TEMP_FILE)
        assert sesh.token['access_token'] == FAKE_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')  # within Oauth2.fetch_token
    @patch('requests.get')
    @patch('webbrowser.open')
    @patch('api_buddy.session.oauth._get_authorization_response_url')
    def test_re_authenticates_if_token_is_expired(self, mock_auth_resp_url, mock_open, mock_get):
        mock_auth_resp_url.return_value = f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        send_request(sesh, prefs, opts, TEMP_FILE)
        assert sesh.token['access_token'] == NEW_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')  # within Oauth2.fetch_token
    @patch('requests.get')
    @patch('webbrowser.open')
    @patch('api_buddy.session.oauth._get_authorization_response_url')
    def test_writes_new_token_if_re_authenticating(self, mock_auth_resp_url, mock_open, mock_get):
        mock_auth_resp_url.return_value = f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        prefs = deepcopy(TEST_PREFERENCES)
        opts = deepcopy(TEST_OPTIONS)
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        send_request(sesh, prefs, opts, TEMP_FILE)
        prefs = load_prefs(TEMP_FILE)
        assert prefs['access_token'] == NEW_ACCESS_TOKEN
