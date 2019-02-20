from schema import (
    Schema,
    SchemaError,
    Optional as Maybe,
    Or
)
from typing import Any, Optional
from urllib.parse import urlparse
from ..typing import Preferences
from ..exceptions import APIBuddyException

DEFAULT_URL_SCHEME = 'https'
DEFAULT_PREFS: Preferences = {
    'redirect_uri': 'http://localhost:8080/',
    'state': None,
    'auth_test_status': 401,
    'api_version': None,
    'access_token': 'can_haz_token',
}


prefs_schema = Schema({
    'api_url': str,
    'client_id': str,
    'client_secret': str,
    'scopes': Schema([str]).validate,
    Maybe(
            'redirect_uri',
            default=DEFAULT_PREFS['redirect_uri'],
        ): str,
    Maybe(
            'state',
            default=DEFAULT_PREFS['state'],
        ): Or(str, None),
    Maybe(
            'auth_test_status',
            default=DEFAULT_PREFS['auth_test_status'],
        ): int,
    Maybe(
            'api_version',
            default=DEFAULT_PREFS['api_version'],
        ): Or(str, None),
    Maybe(
            'access_token',
            default=DEFAULT_PREFS['access_token'],
        ): str,
})


def _validate_api_url(api_url: str) -> str:
    url_parts = urlparse(api_url)
    valid_url = api_url
    if not url_parts.scheme:
        valid_url = f'{DEFAULT_URL_SCHEME}://{api_url}'
    if '?' in api_url:
        raise APIBuddyException(
            title='Your api_url can\'t have query parameters',
            message=f'Did you mean "{valid_url.split("?", 1)}"?',
        )
    if '#' in api_url:
        raise APIBuddyException(
            title='Your api_url can\'t have hash fragments',
            message=f'Did you mean "{valid_url.split("#", 1)}"?',
        )
    return valid_url


def _validate_api_version(api_version: Any) -> Optional[str]:
    if api_version is not None and not isinstance(api_version, str):
        return str(api_version)
    return api_version


def validate_preferences(prefs: Preferences) -> Preferences:
    """Wrap errors nicely"""
    prefs['api_version'] = _validate_api_version(prefs.get('api_version'))
    try:
        valid_prefs: Preferences = prefs_schema.validate(prefs)
    except SchemaError as err:
        raise APIBuddyException(
            title='These preferences are funky',
            message=str(err),
        )
    valid_prefs['api_url'] = _validate_api_url(valid_prefs['api_url'])
    return valid_prefs
