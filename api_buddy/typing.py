from mypy_extensions import TypedDict
from typing import Dict, Iterable, List, Optional, Union

Preferences = TypedDict('Preferences', {
    'api_url': str,
    'client_id': str,
    'client_secret': str,
    'scopes': Iterable[str],
    'redirect_uri': str,  # Optional
    'auth_test_status': int,  # Optional
    'api_version': Optional[str],  # Optional
    'access_token': str,
    'state': Optional[str],  # Optional, can be None
    'absolute_path': str,
}, total=False)

Options = TypedDict('Options', {
    '--help': bool,
    '--version': bool,
    'method': str,
    '<endpoint>': str,
    '<params>': Dict[str, Union[str, List[str]]],
})
