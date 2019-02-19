from mypy_extensions import TypedDict
from typing import Dict, Iterable, List, Optional, Union

Preferences = TypedDict('Preferences', {
    'api_url': str,
    'client_id': str,
    'client_secret': str,
    'scopes': Iterable[str],
    'redirect_uri': str,  # Optional
    'auth_test_path': str,
    'auth_test_status': int,  # Optional
    'access_token': str,
    'state': Optional[str],  # Optional, can be None
}, total=False)

Options = TypedDict('Options', {
    '--help': bool,
    '--version': bool,
    '<endpoint>': str,
    'get': Optional[bool],
    '<params>': Dict[str, Union[str, List[str]]],
})
