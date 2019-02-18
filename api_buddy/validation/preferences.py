from schema import (
    Schema,
    SchemaError,
    Optional,
    Or
)
from ..typing import Preferences
from ..exceptions import APIBuddyException

DEFAULT_PREFS: Preferences = {
    'redirect_uri': 'http://localhost:8080/',
    'state': None,
    'auth_test_status': 401,
    'access_token': 'can_haz_token',
}

prefs_schema = Schema({
    'api_url': str,
    'client_id': str,
    'client_secret': str,
    'scopes': Schema([str]).validate,
    Optional(
            'redirect_uri',
            default=DEFAULT_PREFS['redirect_uri'],
        ): str,
    Optional(
            'state',
            default=DEFAULT_PREFS['state'],
        ): Or(str, None),
    'auth_test_path': str,
    Optional(
            'auth_test_status',
            default=DEFAULT_PREFS['auth_test_status'],
        ): int,
    Optional(
            'access_token',
            default=DEFAULT_PREFS['access_token'],
        ): str,
})


def validate_preferences(prefs: Preferences) -> Preferences:
    """Wrap errors nicely"""
    try:
        valid_prefs: Preferences = prefs_schema.validate(prefs)
    except SchemaError as err:
        raise APIBuddyException(
            title='These preferences are funky',
            message=str(err),
        )
    return valid_prefs
