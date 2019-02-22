from copy import deepcopy
from mock import patch
from requests.exceptions import ConnectionError
from requests_oauthlib import OAuth2Session

from api_buddy.exceptions import APIBuddyException
from api_buddy.session.oauth import get_oauth_session, APPLICATION_JSON
from ..helpers import (
    TEST_PREFERENCES,
    TEST_OPTIONS,
    TEMP_FILE,
    TempYAMLTestCase,
    explode,
    mock_get,
)


class TestGetOauthSession(TempYAMLTestCase):
    @mock_get()
    @patch('requests.get')
    def test_returns_a_session(self, mock_get):
        sesh = get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        assert type(sesh) == OAuth2Session

    @mock_get()
    @patch('requests.get')
    def test_adds_headers(self, mock_get):
        sesh = get_oauth_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        headers = sesh.headers
        assert headers['Accept'] == APPLICATION_JSON
        assert headers['Content-Type'] == APPLICATION_JSON

    @patch('requests.get', side_effect=explode(ConnectionError))
    def test_checks_internet_connection(self, mock_get):
        try:
            get_oauth_session(
                TEST_OPTIONS,
                deepcopy(TEST_PREFERENCES),
                TEMP_FILE,
            )
        except APIBuddyException as err:
            assert 'internet' in err.title
            assert 'WiFi' in err.message
        else:
            assert False
