from colorama import Fore, Style
from schema import (
    Schema,
    SchemaError,
    Optional as Maybe,
    Or
)
from pygments.styles import get_all_styles, get_style_by_name, ClassNotFound
from typing import Any, cast, List, Optional
from urllib.parse import urlparse
from ..utils.formatting import flat_str_dict, format_yaml_list
from ..utils.auth import AUTH_TYPES, OAUTH2
from ..utils.exceptions import PrefsException
from ..utils.http import pack_query_params
from ..utils.typing import Preferences, RawPreferences
from ..config.themes import SHELLECTRIC

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
    'timeout': 60,
    'headers': {},
    'verboseness': DEFAULT_VERBOSENESS_PREFS,
    'indent': 2,
    'theme': SHELLECTRIC,
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
            'timeout',
            default=DEFAULT_PREFS['timeout'],
        ): int,
    Maybe(
            'headers',
            default=DEFAULT_PREFS['headers'],
        ): dict,
    Maybe(
            'verboseness',
            default=DEFAULT_PREFS['verboseness'],
        ): verboseness_schema,
    Maybe(
            'indent',
            default=DEFAULT_PREFS['indent'],
        ): Or(int, None),
    Maybe(
            'theme',
            default=DEFAULT_PREFS['theme'],
        ): Or(str, None),
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
        delim = f'\n  {Fore.BLACK}{Style.BRIGHT}- {Fore.MAGENTA}'
        display_auth_types = (
            delim.join(AUTH_TYPES)
        )
        raise PrefsException(
            title=f'I can\'t recognize your auth_type',
            message=(
                f'It should be one of these:'
                f'{delim}null{delim}'
                f'{display_auth_types}{Style.RESET_ALL}'
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
            message=(
                'Maybe try '
                f'{Fore.BLUE}{Style.BRIGHT}{valid_url.split("?", 1)[0]}'
                f'{Style.RESET_ALL}'
            ),
        )
    if '#' in api_url:
        raise PrefsException(
            title=f'Your api_url can\'t have hash fragments',
            message=(
                'Maybe try '
                f'{Fore.BLUE}{Style.BRIGHT}{valid_url.split("#", 1)[0]}'
                f'{Style.RESET_ALL}'
            ),
        )
    return valid_url


def _validate_api_version(api_version: Any) -> Optional[str]:
    if api_version is not None and not isinstance(api_version, str):
        return str(api_version)
    return api_version


def _validate_theme(theme: Optional[str]) -> Optional[str]:
    if theme is None:
        return None
    elif theme == SHELLECTRIC:
        return SHELLECTRIC
    else:
        try:
            get_style_by_name(theme)
        except ClassNotFound:
            all_styles = [name for name in get_all_styles()]
            all_styles.append(
                f'{SHELLECTRIC} {Fore.BLACK}(this one is coolest)'
            )
            raise PrefsException(
                title=(
                    f'I haven\'t heard of the {Fore.MAGENTA}{theme}'
                    f'{Fore.YELLOW} theme before.'
                ),
                message=(
                    'It sounds cool, but you have to pick one of these '
                    f'instead:\n{format_yaml_list(all_styles)}'
                ),
            )
        return theme


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
    valid_prefs['variables'] = flat_str_dict(
        'variable',
        valid_prefs['variables'],
        check_special_chars=True,
    )
    valid_prefs['oauth2']['authorize_params'] = pack_query_params(
        cast(List[str], valid_prefs['oauth2']['authorize_params']),
    )
    valid_prefs['headers'] = flat_str_dict('header', valid_prefs['headers'])
    valid_prefs['auth_type'] = _validate_auth_type(valid_prefs['auth_type'])
    valid_prefs['theme'] = _validate_theme(valid_prefs['theme'])
    return valid_prefs
