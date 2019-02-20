from os import path, remove
from requests import Response
from unittest import mock, TestCase
from typing import Any, Callable, NoReturn, Optional
from api_buddy.utils import ROOT_DIR
from api_buddy.typing import Preferences, Options

FIXTURES_DIR = path.join(ROOT_DIR, 'tests', 'fixtures')
TEMP_FILE = path.join(FIXTURES_DIR, 'temp.yml')
FAKE_ACCESS_TOKEN = 'banana'
FAKE_API_URL = 'https://fake.api.com'
FAKE_API_VERSION = '3'
FAKE_ENDPOINT = 'cats'
FAKE_STATE = 'california'
TEST_PREFERENCES: Preferences = {
    'api_url': FAKE_API_URL,
    'client_id': 'client_id',
    'client_secret': 'client_secret',
    'scopes': ['a_scope', 'another_scope'],
    'redirect_uri': 'http://localhost:8080/',
    'access_token': FAKE_ACCESS_TOKEN,
    'auth_test_status': 401,
    'api_version': None,
    'state': FAKE_STATE,
}
TEST_OPTIONS: Options = {
    '<endpoint>': FAKE_ENDPOINT,
    '<params>': [],
    'get': True,
    '--help': False,
    '--version': False,
}


def explode(*args: Optional[Any], **kwargs: Optional[Any]) -> NoReturn:
    raise Exception('💣💥')


def _mock_api_method(method: str = 'get') -> Callable[..., Any]:
    """ Wrapper for method-specific api method decorators """
    def decorator_with_args(
                content: str = '{}',
                status_code: int = 200,
            ) -> Callable[..., Any]:
        def real_decorator(
                    func: Callable[..., Any]
                ) -> Callable[..., Any]:
            def wrapper(
                        *args: Optional[Any],
                        **kwargs: Optional[Any]
                    ) -> Any:
                with mock.patch(
                            f'requests_oauthlib.OAuth2Session.{method}'
                        ) as mock_api_call:
                    resp = Response()
                    mock_req = mock.MagicMock()
                    type(mock_req).params = mock.PropertyMock(
                        return_value=kwargs.get('params')
                    )
                    resp.request = mock_req
                    resp.status_code = status_code
                    resp._content = str.encode(content)  # type: ignore
                    mock_api_call.return_value = resp
                    return func(*args, **kwargs)
            return wrapper
        return real_decorator
    return decorator_with_args


def _mock_api_method_side_effect(method: str = 'get') -> Callable[..., Any]:
    """ Wrapper for method-specific api method decorators """
    def decorator_with_args(
                side_effect: Callable[..., Any],
            ) -> Callable[..., Any]:
        def real_decorator(
                    func: Callable[..., Any]
                ) -> Callable[..., Any]:
            def wrapper(
                        *args: Optional[Any],
                        **kwargs: Optional[Any]
                    ) -> Any:
                with mock.patch(
                            f'requests_oauthlib.OAuth2Session.{method}'
                        ) as mock_api_call:
                    mock_api_call.side_effect = side_effect
                    return func(*args, **kwargs)
            return wrapper
        return real_decorator
    return decorator_with_args


# Use these
mock_get = _mock_api_method('get')
mock_post = _mock_api_method('post')
mock_get_side_effect = _mock_api_method_side_effect('get')
mock_post_side_effect = _mock_api_method_side_effect('post')


def clean_temp_yml_file() -> None:
    if path.isfile(TEMP_FILE):
        remove(TEMP_FILE)


class TempYAMLTestCase(TestCase):
    def setUp(self):
        clean_temp_yml_file()

    def tearDown(self):
        clean_temp_yml_file()
