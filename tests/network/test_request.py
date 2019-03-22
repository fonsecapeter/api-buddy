import requests  # noqa
from copy import deepcopy
from mock import MagicMock, PropertyMock, patch
from requests.exceptions import ConnectionError, ReadTimeout
from typing import Any, Dict, List, Union

from api_buddy.config.preferences import load_prefs
from api_buddy.utils.exceptions import (
    APIBuddyException,
    ConnectionException,
    TimeoutException,
)
from api_buddy.network.session import get_session
from api_buddy.network.request import send_request
from api_buddy.utils.http import HTTP_METHODS, GET
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
    mock_patch,
    mock_put,
    mock_delete,
    mock_get_side_effect,
    mock_post_side_effect,
    mock_patch_side_effect,
    mock_put_side_effect,
    mock_delete_side_effect,
    TempYAMLTestCase,
)

NEW_ACCESS_TOKEN = 'mint-chip'


def _mock_param_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {},
            timeout: int = 0,
            verify: bool = True,
        ):
    mock_resp = MagicMock()
    type(mock_resp).params = PropertyMock(return_value=params)
    return mock_resp


def _mock_url_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {},
            timeout: int = 0,
            verify: bool = True,
        ):
    mock_resp = MagicMock()
    type(mock_resp).url = PropertyMock(return_value=url)
    return mock_resp


def _mock_data_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {},
            data: Any = None,
            timeout: int = 0,
            verify: bool = True,
        ):
    mock_resp = MagicMock()
    type(mock_resp).data = PropertyMock(return_value=data)
    return mock_resp


def _mock_verify_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {},
            data: Any = None,
            timeout: int = 0,
            verify: bool = True,
        ):
    mock_resp = MagicMock()
    type(mock_resp).verify = PropertyMock(return_value=verify)
    return mock_resp


class TestSendRequest(TempYAMLTestCase):
    def setUp(self):
        self.prefs = deepcopy(TEST_PREFERENCES)
        self.prefs['auth_type'] = None
        self.opts = deepcopy(TEST_OPTIONS)
        self.sesh = get_session(self.opts, self.prefs, TEMP_FILE)
        super().setUp()

    @mock_get_side_effect(explode(ConnectionError))
    def test_checks_internet_connection(self):
        try:
            send_request(
                self.sesh,
                self.prefs,
                self.opts,
                TEMP_FILE,
            )
        except ConnectionException:
            assert True
        else:
            assert False

    @mock_get_side_effect(explode(ReadTimeout))
    def test_can_timeout_on_internet_connection(self):
        try:
            send_request(
                self.sesh,
                self.prefs,
                self.opts,
                TEMP_FILE,
            )
        except TimeoutException:
            assert True
        else:
            assert False

    @mock_get()
    @patch('requests.get')
    def test_returns_a_response(self, mock_get):
        mock_resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert mock_resp.status_code == 200

    @mock_get('{"get": true}')
    @mock_post('{"post": true}')
    @mock_patch('{"patch": true}')
    @mock_put('{"put": true}')
    @mock_delete('{"delete": true}')
    @patch('requests.get')
    def test_checks_method(self, mock_get):
        for method in HTTP_METHODS:
            self.opts['<method>'] = method
            resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
            assert resp.json()[method] is True

    @mock_get()
    @patch('requests.get')
    def test_if_method_isnt_off_it_blows_up(self, mock_get):
        self.opts['<method>'] = 'banana'
        try:
            send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        except APIBuddyException as err:
            assert 'went wrong' in err.title
            assert 'http method' in err.message
        else:
            assert False

    @patch('requests.get')
    @mock_get_side_effect(_mock_url_catcher)
    def test_adds_endpoint_to_api_url(self, mock_get):
        mock_resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert mock_resp.url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}'

    @patch('requests.get')
    @mock_get_side_effect(_mock_param_catcher)
    def test_uses_params(self, mock_get):
        params = {'fake_param': 'fake_value'}
        self.opts['<params>'] = params
        mock_resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert mock_resp.params == params

    @patch('requests.get')
    @mock_get_side_effect(_mock_url_catcher)
    def test_uses_api_version_if_given(self, mock_get):
        params = {'fake_param': 'fake_value'}
        self.prefs['api_version'] = FAKE_API_VERSION
        self.opts['<params>'] = params
        mock_resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert (
            mock_resp.url
            == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}'
        )

    @mock_get_side_effect(_mock_data_catcher)
    @mock_post_side_effect(_mock_data_catcher)
    @mock_put_side_effect(_mock_data_catcher)
    @mock_patch_side_effect(_mock_data_catcher)
    @mock_delete_side_effect(_mock_data_catcher)
    @patch('requests.get')
    def test_adds_data_to_requests(self, mock_get):
        data = '{"dis":"json"}'
        self.opts['<data>'] = data
        for method in HTTP_METHODS:
            self.opts['<method>'] = method
            mock_resp = send_request(
                self.sesh,
                self.prefs,
                self.opts,
                TEMP_FILE
            )
            if method == GET:
                assert mock_resp.data is None
            else:
                assert mock_resp.data == data

    @mock_get()
    @mock_post()
    @patch('requests.get')
    def test_can_print_request_details(self, mock_get):
        self.opts['<params>'] = {
            'name': 'george-costanza',
            'occupations': [
                'architect',
                'marine-biologist',
            ],
            'has_hair': 'false',
        }
        self.opts['<data>'] = {
            'name': 'Cosmo Kramer',
            'occupations': [
                'Bagelrista',
                'Car Parker',
            ],
            'has_hair': True,
        }
        self.opts['<method>'] = 'post'
        self.prefs['verboseness']['request'] = True
        # should not raise any errors
        send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)

    @mock_get_side_effect(_mock_verify_catcher)
    @patch('requests.get')
    def test_honors_verify_prefs(self, mock_get):
        mock_resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert mock_resp.verify is True
        self.prefs['verify_ssl'] = False
        mock_resp = send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert mock_resp.verify is False


class TestSendOAuth2Request(TempYAMLTestCase):
    def setUp(self):
        self.prefs = deepcopy(TEST_PREFERENCES)
        self.opts = deepcopy(TEST_OPTIONS)
        self.sesh = get_session(self.opts, self.prefs, TEMP_FILE)
        super().setUp()

    @mock_get()
    @patch('requests.get')
    @patch('api_buddy.network.auth.oauth2._authenticate')
    def test_skips_authentication_if_token_is_valid(
                self, mock_authenticate, mock_get
            ):
        mock_authenticate.side_effect = explode()  # should not get called
        send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert self.sesh.token['access_token'] == FAKE_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')
    @patch('requests.get')
    @patch('webbrowser.open')
    @patch('api_buddy.network.auth.oauth2._get_authorization_response_url')
    def test_re_authenticates_if_token_is_expired(
                self, mock_auth_resp_url, mock_open, mock_get
            ):
        mock_auth_resp_url.return_value = (
            f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        )
        send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        assert self.sesh.token['access_token'] == NEW_ACCESS_TOKEN

    @mock_get(status_code=401)  # expired token check
    @mock_post(content=f'{{"access_token": "{NEW_ACCESS_TOKEN}"}}')
    @patch('requests.get')
    @patch('webbrowser.open')
    @patch('api_buddy.network.auth.oauth2._get_authorization_response_url')
    def test_writes_new_token_if_re_authenticating(
                self, mock_auth_resp_url, mock_open, mock_get
            ):
        mock_auth_resp_url.return_value = (
            f'{FAKE_API_URL}/?code=banana&state={FAKE_STATE}'
        )
        send_request(self.sesh, self.prefs, self.opts, TEMP_FILE)
        prefs = load_prefs(TEMP_FILE)
        assert prefs['oauth2']['access_token'] == NEW_ACCESS_TOKEN
