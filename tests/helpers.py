from os import path, remove
from requests import Response
from unittest import mock, TestCase
from typing import Any, Callable, NoReturn, Optional
from api_buddy.utils import ROOT_DIR
from api_buddy.utils.typing import Preferences, Options
from api_buddy.config.themes import SHELLECTRIC

FIXTURES_DIR = path.join(ROOT_DIR, 'tests', 'fixtures')
TEMP_FILE = path.join(FIXTURES_DIR, 'temp.yml')
FAKE_ACCESS_TOKEN = 'banana'
FAKE_API_URL = 'https://fake.api.com'
FAKE_API_VERSION = '3'
FAKE_ENDPOINT = 'cats'
FAKE_STATE = 'california'
TEST_PREFERENCES: Preferences = {
    'api_url': FAKE_API_URL,
    'auth_type': 'oauth2',
    'oauth2': {
        'client_id': 'client_id',
        'client_secret': 'client_secret',
        'scopes': ['a_scope', 'another_scope'],
        'redirect_uri': 'http://localhost:8080/',
        'access_token': FAKE_ACCESS_TOKEN,
        'state': FAKE_STATE,
        'token_path': 'token',
        'authorize_path': 'authorize',
        'authorize_params': {},
    },
    'auth_test_status': 401,
    'api_version': None,
    'verify_ssl': True,
    'timeout': 60,
    'headers': {},
    'verboseness': {
        'request': False,
        'response': False,
    },
    'indent': 2,
    'theme': SHELLECTRIC,
    'variables': {},
}
TEST_OPTIONS: Options = {
    '<method>': 'get',
    '<endpoint>': FAKE_ENDPOINT,
    '<params>': {},
    '<data>': None,
    '--help': False,
    '--version': False,
}


def explode(err: Exception = Exception) -> Callable[..., Any]:
    def wrapper(*args: Optional[Any], **kwargs: Optional[Any]) -> NoReturn:
        raise err('💣💥')
    return wrapper


def _mock_api_method(method: str = 'get') -> Callable[..., Any]:
    """Wrapper for method-specific api method decorators

    With response content and status code values
    """
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
                            f'requests.Session.{method}'
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
    """Wrapper for method-specific api method decorators

    With side effects
    """
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
                            f'requests.Session.{method}'
                        ) as mock_api_call:
                    mock_api_call.side_effect = side_effect
                    return func(*args, **kwargs)
            return wrapper
        return real_decorator
    return decorator_with_args


# Use these
mock_get = _mock_api_method('get')
mock_post = _mock_api_method('post')
mock_put = _mock_api_method('put')
mock_patch = _mock_api_method('patch')
mock_delete = _mock_api_method('delete')
mock_get_side_effect = _mock_api_method_side_effect('get')
mock_post_side_effect = _mock_api_method_side_effect('post')
mock_put_side_effect = _mock_api_method_side_effect('put')
mock_patch_side_effect = _mock_api_method_side_effect('patch')
mock_delete_side_effect = _mock_api_method_side_effect('delete')


def clean_temp_yml_file() -> None:
    if path.isfile(TEMP_FILE):
        remove(TEMP_FILE)


class TempYAMLTestCase(TestCase):
    def setUp(self):
        clean_temp_yml_file()

    def tearDown(self):
        clean_temp_yml_file()
