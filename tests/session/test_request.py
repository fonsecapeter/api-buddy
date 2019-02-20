from copy import deepcopy
from mock import MagicMock, PropertyMock
from typing import Dict, List, Union
from api_buddy.exceptions import APIBuddyException
from api_buddy.session.oauth import get_oauth_session
from api_buddy.session.request import send_request
from ..helpers import (
    TEST_PREFERENCES,
    TEMP_FILE,
    mock_get,
    mock_get_side_effect,
    TempYAMLTestCase,
)


def _mock_param_catcher(
            url: str,
            params: Dict[str, Union[str, List[str]]] = {}
        ):
    mock_resp = MagicMock()
    type(mock_resp).params = PropertyMock(return_value=params)
    return mock_resp


class TestSendRequest(TempYAMLTestCase):
    @mock_get()
    def test_returns_a_resopnse(self):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = {
            '<endpoint>': 'fake_endpoint',
            '<params>': {},
            'get': True,
            '--help': False,
            '--version': False,
        }
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        resp = send_request(sesh, prefs, opts)
        assert resp.status_code == 200

    @mock_get()
    def test_checks_method(self):
        prefs = deepcopy(TEST_PREFERENCES)
        opts = {
            '<endpoint>': 'fake_endpoint',
            '<params>': {},
            'get': False,
            '--help': False,
            '--version': False,
        }
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        try:
            send_request(sesh, prefs, opts)
        except APIBuddyException as err:
            assert 'went wrong' in err.title
            assert 'http method' in err.message
        else:
            assert False

    @mock_get_side_effect(_mock_param_catcher)
    def test_uses_params(self):
        params = {'fake_param': 'fake_value'}
        prefs = deepcopy(TEST_PREFERENCES)
        opts = {
            '<endpoint>': 'fake_endpoint',
            '<params>': params,
            'get': True,
            '--help': False,
            '--version': False,
        }
        sesh = get_oauth_session(opts, prefs, TEMP_FILE)
        mock_resp = send_request(sesh, prefs, opts)
        assert mock_resp.params == params
