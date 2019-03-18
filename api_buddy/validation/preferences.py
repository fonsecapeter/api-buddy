from schema import (
    Schema,
    SchemaError,
    Optional as Maybe,
    Or
)
from typing import Any, cast, List, Optional
from urllib.parse import urlparse
from ..utils import flat_str_dict, UtilException
from ..utils.typing import Preferences, RawPreferences
from ..utils.exceptions import PrefsException
from ..utils.auth import AUTH_TYPES, OAUTH2
from ..utils.http import pack_query_params

DEFAULT_URL_SCHEME = 'https'
DEFAULT_OAUTH2_PREFS = {
    'redirect_uri': 'http://localhost:8080/',
    'state': None,
    'access_token': 'can_haz_token',
    'token_path': 'token',
    'authorize_path': 'authorize',
    'authorize_params': {},
}
DEFAULT_VERBOSENESS_PREFS = {
    'request': False,
    'response': False,
}
DEFAULT_PREFS = {
    'auth_type': None,
    'oauth2': DEFAULT_OAUTH2_PREFS,
    'auth_test_status': 401,
    'api_version': None,
    'verify_ssl': True,
    'headers': {},
    'verboseness': DEFAULT_VERBOSENESS_PREFS,
    'variables': {},
}
DEFAULT_AUTH_PREFS = {
    OAUTH2: DEFAULT_OAUTH2_PREFS,
}
NESTED_DEFAULT_PREFS = {
    **DEFAULT_AUTH_PREFS,  # type: ignore
    'verboseness': DEFAULT_VERBOSENESS_PREFS,
}


oauth2_schema = Schema({
    'client_id': str,
    'client_secret': str,
    'scopes': Schema([str]).validate,
    Maybe(
            'redirect_uri',
            default=DEFAULT_OAUTH2_PREFS['redirect_uri'],
        ): str,
    Maybe(
            'state',
            default=DEFAULT_OAUTH2_PREFS['state'],
        ): Or(str, None),
    Maybe(
            'access_token',
            default=DEFAULT_OAUTH2_PREFS['access_token'],
        ): str,
    Maybe(
            'token_path',
            default=DEFAULT_OAUTH2_PREFS['token_path'],
        ): str,
    Maybe(
            'authorize_path',
            default=DEFAULT_OAUTH2_PREFS['authorize_path'],
        ): str,
    Maybe(
            'authorize_params',
            default=DEFAULT_OAUTH2_PREFS['authorize_params'],
        ): [str],
})

verboseness_schema = Schema({
    Maybe(
            'request',
            default=DEFAULT_VERBOSENESS_PREFS['request'],
        ): bool,
    Maybe(
            'response',
            default=DEFAULT_VERBOSENESS_PREFS['response'],
        ): bool,
})

prefs_schema = Schema({
    'api_url': str,
    Maybe(
            'auth_type',
            default=DEFAULT_PREFS['auth_type'],
        ): Or(str, None),
    Maybe(
            'oauth2',
            default=DEFAULT_PREFS['oauth2'],
        ): oauth2_schema,
    Maybe(
            'auth_test_status',
            default=DEFAULT_PREFS['auth_test_status'],
        ): int,
    Maybe(
            'api_version',
            default=DEFAULT_PREFS['api_version'],
        ): Or(str, int, float, None),
    Maybe(
            'verify_ssl',
            default=DEFAULT_PREFS['verify_ssl'],
        ): bool,
    Maybe(
            'headers',
            default=DEFAULT_PREFS['headers'],
        ): dict,
    Maybe(
            'verboseness',
            default=DEFAULT_PREFS['verboseness'],
        ): verboseness_schema,
    Maybe(
            'variables',
            default=DEFAULT_PREFS['variables'],
        ): dict,
})


def _validate_auth_type(auth_type: Optional[str]) -> Optional[str]:
    if auth_type is None:
        return None
    valid_auth_type = auth_type.lower()
    if valid_auth_type not in AUTH_TYPES:
        display_auth_types = '  - '.join(AUTH_TYPES)
        raise PrefsException(
            title=f'I can\'t recognize your auth_type',
            message=(
                f'It should be one of these:\n'
                f'  - null\n  - {display_auth_types}'
            ),
        )
    return valid_auth_type


def _validate_api_url(api_url: str) -> str:
    url_parts = urlparse(api_url)
    valid_url = api_url
    if not url_parts.scheme:
        valid_url = f'{DEFAULT_URL_SCHEME}://{api_url}'
    if '?' in api_url:
        raise PrefsException(
            title=f'Your api_url can\'t have query parameters',
            message=f'Did you mean "{valid_url.split("?", 1)}"?',
        )
    if '#' in api_url:
        raise PrefsException(
            title=f'Your api_url can\'t have hash fragments',
            message=f'Did you mean "{valid_url.split("#", 1)}"?',
        )
    return valid_url


def _validate_api_version(api_version: Any) -> Optional[str]:
    if api_version is not None and not isinstance(api_version, str):
        return str(api_version)
    return api_version


def validate_preferences(prefs: RawPreferences) -> Preferences:
    """Wrap errors nicely"""
    prefs['api_version'] = _validate_api_version(prefs.get('api_version'))
    try:
        valid_prefs: Preferences = prefs_schema.validate(prefs)
    except SchemaError as err:
        raise PrefsException(
            title='Something doesn\'t match the schema',
            message=str(err),
        )
    valid_prefs['api_url'] = _validate_api_url(valid_prefs['api_url'])
    try:
        valid_prefs['variables'] = flat_str_dict(
            'variables',
            valid_prefs['variables'],
            check_special_chars=True,
        )
    except UtilException as err:
        raise PrefsException(title=err.title, message=err.message)
    valid_prefs['oauth2']['authorize_params'] = pack_query_params(
        cast(List[str], valid_prefs['oauth2']['authorize_params']),
    )
    valid_prefs['headers'] = flat_str_dict('headers', valid_prefs['headers'])
    valid_prefs['auth_type'] = _validate_auth_type(valid_prefs['auth_type'])
    return valid_prefs
