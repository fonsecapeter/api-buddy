from mypy_extensions import TypedDict
from typing import Any, Dict, Iterable, List, Optional, Union

VerbosenessPreferences = TypedDict('VerbosenessPreferences', {
    'request': bool,
    'response': bool,
})

QueryParams = Dict[str, Union[str, List[str]]]
OAuth2Preferences = TypedDict('OAuth2Preferences', {
    'client_id': str,
    'client_secret': str,
    'scopes': Iterable[str],
    'redirect_uri': str,
    'access_token': str,
    'state': Optional[str],
    'token_path': str,
    'authorize_path': str,
    'authorize_params': QueryParams,
})

RawPreferences = Dict[str, Any]
Preferences = TypedDict('Preferences', {
    'api_url': str,
    'auth_type': Optional[str],
    'oauth2': OAuth2Preferences,
    'auth_test_status': int,
    'api_version': Optional[str],
    'verify_ssl': bool,
    'timeout': int,
    'headers': Dict[str, str],
    'verboseness': VerbosenessPreferences,
    'indent': Optional[int],
    'theme': Optional[str],
    'variables': Dict[str, str],
})


Options = TypedDict('Options', {
    '--help': bool,
    '--version': bool,
    '<method>': str,
    '<endpoint>': str,
    '<params>': QueryParams,
    '<data>': Any,
})

RawOptions = Dict[str, Optional[Union[str, bool]]]
# TypedDict currently requires string literal key indexing
# RawOptions = TypedDict('RawOptions', {
#     '--help': bool,
#     '--version': bool,
#     'help': bool,
#     'get': bool,
#     'post': bool,
#     'patch': bool,
#     'put': bool,
#     'delete': bool,
#     '<endpoint>': str,
#     '<params>': List[str],
#     '<data>': Optional[str],
# })
