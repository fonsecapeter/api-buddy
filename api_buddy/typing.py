from mypy_extensions import TypedDict
from typing import Any, Dict, Iterable, List, Optional, Union

VerbosenessPreferences = TypedDict('VerbosenessPreferences', {
    'request': bool,
    'response': bool,
})

Preferences = TypedDict('Preferences', {
    'api_url': str,
    'client_id': str,
    'client_secret': str,
    'scopes': Iterable[str],
    'redirect_uri': str,
    'auth_test_status': int,
    'api_version': Optional[str],
    'access_token': str,
    'state': Optional[str],
    'verboseness': VerbosenessPreferences,
    'variables': Dict[str, str],
}, total=False)

Options = TypedDict('Options', {
    '--help': bool,
    '--version': bool,
    '<method>': str,
    '<endpoint>': str,
    '<params>': Dict[str, Union[str, List[str]]],
    '<data>': Any,
})

RawOptions = Dict[str, Optional[Union[str, bool]]]
# TypedDict currently requires string literal key indexing
# RawOptions = TypedDict('RawOptions', {
#     '--help': bool,
#     '--version': bool,
#     '<method>': str,  # added in validation
#     'get': bool,
#     'post': bool,
#     'patch': bool,
#     'put': bool,
#     'delete': bool,
#     '<endpoint>': str,
#     '<params>': List[str],
#     '<data>': Optional[str],
# }, total=False)
