from copy import deepcopy
from mock import patch, Mock
from api_buddy.network.session import (
    REAUTHENTICATIONS,
    SESSIONS,
    get_session,
    reauthenticate,
)
from api_buddy.utils.auth import OAUTH2
from ..helpers import (
    TEST_PREFERENCES,
    TEST_OPTIONS,
    TEMP_FILE,
    TempYAMLTestCase,
)

mock_get_oauth2_sesh = Mock(name='mock_get_oauth2_sesh')
mock_reauth2 = Mock(name='mock_reauth2')


class TestGetSession(TempYAMLTestCase):
    def setUp(self):
        self.prefs = deepcopy(TEST_PREFERENCES)
        self.opts = deepcopy(TEST_OPTIONS)
        super().setUp()

    @patch('requests.Session')
    def test_can_instantiate_with_no_auth(
                self,
                mock_requests_session,
            ):
        self.prefs['auth_type'] = None
        with patch.dict(
                    SESSIONS,
                    {OAUTH2: mock_get_oauth2_sesh},
                    clear=True
                ):
            get_session(self.opts, self.prefs, TEMP_FILE)
            assert mock_requests_session.called_once()
            assert mock_get_oauth2_sesh.not_called()

    @patch('requests.Session')
    def test_when_using_an_auth_type_it_checks_preferences(
                self,
                mock_requests_session,
            ):
        with patch.dict(
                    SESSIONS,
                    {OAUTH2: mock_get_oauth2_sesh},
                    clear=True
                ):
            get_session(self.opts, self.prefs, TEMP_FILE)
            assert mock_get_oauth2_sesh.called_once()
            assert mock_requests_session.not_called()


class TestReauthenticate(TempYAMLTestCase):
    def setUp(self):
        self.prefs = deepcopy(TEST_PREFERENCES)
        self.opts = deepcopy(TEST_OPTIONS)
        self.session = get_session(self.opts, self.prefs, TEMP_FILE)
        super().setUp()

    @patch('api_buddy.network.session.reauthenticate_oauth2')
    def test_when_using_no_auth_it_does_nothing(self, mock_reauth):
        self.prefs['auth_type'] = None
        with patch.dict(
                    REAUTHENTICATIONS,
                    {OAUTH2: mock_reauth2},
                    clear=True
                ):
            reauthenticate(self.session, self.prefs, TEMP_FILE)
            assert mock_reauth.not_called()

    def test_when_using_an_auth_type_it_checks_preferences(self):
        with patch.dict(
                    REAUTHENTICATIONS,
                    {OAUTH2: mock_reauth2},
                    clear=True
                ):
            reauthenticate(self.session, self.prefs, TEMP_FILE)
            assert mock_reauth2.called_once()
