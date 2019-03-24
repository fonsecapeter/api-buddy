import yaml
from os import path
from copy import deepcopy
from typing import Any

from ..utils.exceptions import PrefsException
from ..utils.http import unpack_query_params
from ..utils.typing import Preferences
from ..validation.preferences import (
    DEFAULT_PREFS,
    NESTED_DEFAULT_PREFS,
    validate_preferences,
)

EXAMPLE_OAUTH2_PREFS = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',
    'scopes': ['one_scope', 'another_scope'],
}
EXAMPLE_PREFS = {
    'api_url': 'https://ron-swanson-quotes.herokuapp.com',
}


def _remove_defaults(prefs: Preferences) -> Preferences:
    """Remove defaults if they haven't been changed"""
    filtered_prefs = deepcopy(prefs)
    for key, default_val in DEFAULT_PREFS.items():
        if key in NESTED_DEFAULT_PREFS:
            continue
        if filtered_prefs[key] == default_val:                 # type: ignore
            del filtered_prefs[key]                            # type: ignore
    for nested_name, nested_defaults in NESTED_DEFAULT_PREFS.items():
        nested_prefs = filtered_prefs[nested_name]             # type: ignore
        for nested_key, default_nested_val in nested_defaults.items():
            if nested_prefs[nested_key] == default_nested_val:
                del filtered_prefs[nested_name][nested_key]    # type: ignore
    return filtered_prefs


def _convert_types(prefs: Preferences) -> Preferences:
    """Convert any types that are changed in validation for saving"""
    converted_prefs = deepcopy(prefs)
    auth_prefs = converted_prefs.get('oauth2')
    if auth_prefs:
        auth_params = auth_prefs.get('authorize_params')
        if auth_params:
            converted_prefs['oauth2']['authorize_params'] = (  # type: ignore
                unpack_query_params(auth_params)
            )
    return converted_prefs


def _extract_yaml_from_file(file_name: str) -> Any:
    """Load contents of yaml file

    Retuns:
        - None if file doesn't exist
        - The python-native data if it does

    Raises:
        PrefsException if:
            - file contents are not valid yaml
            - user preferences are None
    """
    if not path.isfile(file_name):
        return None
    with open(file_name, 'r') as prefs_file:
        try:
            user_prefs = yaml.load(prefs_file)
        except yaml.YAMLError:
            raise PrefsException(
                title=f'There was a problem reading the file',
                message=(
                    'Please make sure it\'s valid yaml: '
                    'http://www.yaml.org/start.html'
                ),
            )
    if user_prefs is None:
        raise PrefsException(
            title='It looks like your file is empty',
            message=(
                f'Make sure you have something in there\n'
                f'For example:\n\n{yaml.dump(EXAMPLE_PREFS)}'
            )
        )
    return user_prefs


def load_prefs(
            file_name: str,
        ) -> Preferences:
    """Load preferences from a yaml file

    Notes:
        - Expands ~
        - Creates a preferences file if it doesn't exist
        - Merges with defaults
    """
    expanded_file_name = path.expanduser(file_name)
    raw_prefs = _extract_yaml_from_file(expanded_file_name)
    if raw_prefs is None:
        prefs = validate_preferences(EXAMPLE_PREFS)
        save_prefs(prefs, expanded_file_name)
    else:
        prefs = validate_preferences(raw_prefs)
    return prefs


def save_prefs(
            preferences: Preferences,
            file_name: str,
        ) -> None:
    """Save preferences as a yaml file

    Notes:
        - Expands ~
        - Ignores defaults if they haven't changed
    """
    expanded_file_name = path.expanduser(file_name)
    minimal_prefs = _remove_defaults(preferences)
    converted_prefs = _convert_types(minimal_prefs)
    with open(expanded_file_name, 'w') as prefs_file:
        yaml.dump(converted_prefs, prefs_file)
