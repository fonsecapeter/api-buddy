from copy import deepcopy
from mock import patch
from requests_oauthlib import OAuth2Session

from api_buddy.network.auth.oauth2 import get_oauth2_session, APPLICATION_JSON
from tests.helpers import (
    TEST_PREFERENCES,
    TEST_OPTIONS,
    TEMP_FILE,
    TempYAMLTestCase,
    mock_get,
)


class TestGetOauthSession(TempYAMLTestCase):
    @mock_get()
    @patch('requests.get')
    def test_returns_a_session(self, mock_get):
        sesh = get_oauth2_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        assert isinstance(sesh, OAuth2Session)

    @mock_get()
    @patch('requests.get')
    def test_adds_headers(self, mock_get):
        sesh = get_oauth2_session(
            TEST_OPTIONS,
            deepcopy(TEST_PREFERENCES),
            TEMP_FILE,
        )
        headers = sesh.headers
        assert headers['Accept'] == APPLICATION_JSON
        assert headers['Content-Type'] == APPLICATION_JSON
