from copy import deepcopy
from api_buddy.exceptions import APIBuddyException
from api_buddy.session.oauth import get_oauth_session
from api_buddy.session.request import send_request
from ..helpers import (
    TEST_PREFERENCES,
    TEMP_FILE,
    mock_get,
    TempYAMLTestCase,
)


class TestSendRequest(TempYAMLTestCase):
    @mock_get()
    def test_returns_a_resopnse(self):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = {
            '<endpoint>': 'fake_endpoint',
            'get': True,
            '--help': False,
            '--version': False,
        }
        sesh = get_oauth_session(prefs, TEMP_FILE)
        resp = send_request(sesh, prefs, opts)
        assert resp.status_code == 200

    @mock_get()
    def test_checks_method(self):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = {
            '<endpoint>': 'fake_endpoint',
            'get': False,
            '--help': False,
            '--version': False,
        }
        sesh = get_oauth_session(prefs, TEMP_FILE)
        try:
            send_request(sesh, prefs, opts)
        except APIBuddyException as err:
            assert 'went wrong' in err.title
            assert 'http method' in err.message
