from requests import Response
from unittest import mock
from typing import Any, Callable, Dict, NoReturn, Optional


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
                with mock.patch(f'requests_oauthlib.OAuth2Session.{method}') as mock_api_call:
                    resp = Response()
                    resp.request = mock.MagicMock()
                    resp.status_code = status_code
                    resp._content = str.encode(content)  # type: ignore
                    mock_api_call.return_value = resp
                    return func(*args, **kwargs)
            return wrapper
        return real_decorator
    return decorator_with_args


# Use these
mock_get = _mock_api_method('get')
mock_post = _mock_api_method('post')
