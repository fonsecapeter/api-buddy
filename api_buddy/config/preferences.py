import yaml
from os import path
from copy import deepcopy
from typing import Any

from ..exceptions import APIBuddyException
from ..typing import Preferences
from ..validation.preferences import DEFAULT_PREFS, validate_preferences

EXAMPLE_PREFS: Preferences = {
    'api_url': 'https://jsonplaceholder.typicode.com',
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',
    'scopes': ['one_scope', 'another_scope'],
    'redirect_uri': DEFAULT_PREFS['redirect_uri'],
    'auth_test_path': 'endpoint_that_requires_token',
}


def _remove_defaults(prefs: Preferences) -> Preferences:
    """Remove defaults if they haven't been changed"""
    filtered_prefs = deepcopy(prefs)
    for key, default_val in DEFAULT_PREFS.items():
        if filtered_prefs[key] == default_val:  # type: ignore
            del filtered_prefs[key]             # type: ignore
    return filtered_prefs


def _extract_yaml_from_file(file_name: str) -> Any:
    """Load contents of yaml file

    Retuns:
        - None if file doesn't exist
        - The python-native data if it does

    Raises:
        APIBuddyException if:
            - file contents are not valid yaml
            - user preferences are None
    """
    if not path.isfile(file_name):
        return None
    with open(file_name, 'r') as prefs_file:
        try:
            user_prefs = yaml.load(prefs_file)
        except yaml.YAMLError:
            raise APIBuddyException(
                title=f'There was a problem reading {file_name}',
                message=(
                    'Please make sure it\'s valid yaml: '
                    'http://www.yaml.org/start.html'
                ),
            )
    if user_prefs is None:
        raise APIBuddyException(
            title='It looks like your preferences are empty',
            message=(
                f'You should put them in {file_name}\n'
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
    with open(expanded_file_name, 'w') as prefs_file:
        yaml.dump(_remove_defaults(preferences), prefs_file)
