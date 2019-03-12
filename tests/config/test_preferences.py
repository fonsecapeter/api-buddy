import yaml
from os import path
from api_buddy.exceptions import APIBuddyException
from api_buddy.typing import Preferences
from api_buddy.utils import OAUTH2, AUTH_TYPES
from api_buddy.validation.preferences import (
    DEFAULT_PREFS,
    DEFAULT_OAUTH2_PREFS,
)
from api_buddy.config.preferences import (
    EXAMPLE_PREFS,
    EXAMPLE_OAUTH2_PREFS,
    load_prefs,
    save_prefs,
)
from ..helpers import (
    FIXTURES_DIR,
    TEMP_FILE,
    TempYAMLTestCase,
)


LOADED_MSG = 'Preferences loaded just fine:\n'
CAT_FACTS_API_URL = 'https://cat-facts.com'
NEW_PREFS: Preferences = {
    'api_url': 'https://thecatapi.com',
    'auth_type': OAUTH2,
    'oauth2': {
        'client_id': 'mittens',
        'client_secret': 'whiskers',
        'redirect_uri': 'http://localhost:8080/',
        'scopes': ['keyboards', 'stuck_in_boxes'],
        'state': None,
        'access_token': 'feline_token',
    },
    'auth_test_status': 401,
    'api_version': None,
    'verify_ssl': True,
    'verboseness': {
        'request': False,
        'response': False,
    },
    'variables': {},
}


def _fixture_path(file_name):
    abs_path = path.join(FIXTURES_DIR, file_name)
    assert path.isfile(abs_path), f'There\'s no fixtures named "{file_name}"'
    return abs_path


class TestLoadPreferences(TempYAMLTestCase):
    def test_can_load_from_a_yaml_file(self):
        prefs = load_prefs(_fixture_path('test.yml'))
        assert prefs['api_url'] == 'https://api.doggos.com'
        assert prefs['oauth2']['client_id'] == 'my_favorite_client_id'
        assert prefs['oauth2']['client_secret'] == 'my_favorite_client_secret'
        assert prefs['oauth2']['scopes'] == ['dogs', 'kibbles']
        assert prefs['oauth2']['state'] is None
        assert prefs['auth_test_status'] == 403

    def test_merges_yaml_with_defaults(self):
        prefs = load_prefs(_fixture_path('test.yml'))
        # retains non-default
        assert prefs['oauth2']['client_id'] == 'my_favorite_client_id'
        # not specified
        assert (
            prefs['oauth2']['redirect_uri']
            == DEFAULT_OAUTH2_PREFS['redirect_uri']
        )
        # not specified
        assert prefs['api_version'] == DEFAULT_PREFS['api_version']
        # overwritten default
        assert prefs['auth_test_status'] == 403

    def test_when_file_doesnt_exist_it_writes_example_prefs(self):
        assert not path.isfile(TEMP_FILE)
        prefs = load_prefs(TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        for key, example_val in EXAMPLE_PREFS.items():
            if key in AUTH_TYPES:
                continue
            assert prefs[key] == example_val
        for key, example_val in EXAMPLE_OAUTH2_PREFS.items():
            assert prefs['oauth2'][key] == example_val

    def test_file_must_contain_valid_yaml(self):
        try:
            prefs = load_prefs(_fixture_path('bad.yml'))
        except APIBuddyException as err:
            assert 'problem reading' in err.title
            assert 'valid yaml' in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_file_cant_be_empty(self):
        try:
            prefs = load_prefs(_fixture_path('empty.yml'))
        except APIBuddyException as err:
            assert 'preferences are empty' in err.title
            assert (
                f'client_id: {EXAMPLE_PREFS["oauth2"]["client_id"]}'
                in err.message
            )
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_validates_field_types(self):
        try:
            prefs = load_prefs(_fixture_path('bad_types.yml'))
        except APIBuddyException as err:
            assert 'preferences are funky' in err.title
            assert 'client_id' in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_validates_required_fields(self):
        try:
            prefs = load_prefs(_fixture_path('missing_fields.yml'))
        except APIBuddyException as err:
            assert 'preferences are funky' in err.title
            assert 'api_url' in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_adds_default_api_url_scheme_if_missing(self):
        prefs = load_prefs(_fixture_path('api_url_without_scheme.yml'))
        assert prefs['api_url'] == CAT_FACTS_API_URL

    def test_doesnt_allow_query_string_in_api_url(self):
        try:
            prefs = load_prefs(_fixture_path('api_url_with_query_string.yml'))
        except APIBuddyException as err:
            assert 'query parameters' in err.title
            # helpful suggestion
            assert CAT_FACTS_API_URL in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_doesnt_allow_hash_fragments_in_api_url(self):
        try:
            prefs = load_prefs(_fixture_path('api_url_with_hash_fragment.yml'))
        except APIBuddyException as err:
            assert 'hash fragments' in err.title
            # helpful suggestion
            assert CAT_FACTS_API_URL in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_supports_string_api_versions(self):
        prefs = load_prefs(_fixture_path('api_version_as_str.yml'))
        assert prefs['api_version'] == 'three'

    def test_when_api_version_is_not_none_it_coerces_to_str(self):
        prefs = load_prefs(_fixture_path('api_version_as_int.yml'))
        assert prefs['api_version'] == '3'

    def test_loads_variables_as_strings(self):
        prefs = load_prefs(_fixture_path('happy_variables.yml'))
        assert prefs['variables'] == {
            'simle_str': 'is probably most common',
            'ints': '2',
            '3': '3',  # keys are stringified too
            'true': 'true',  # bools should be quoted
        }

    def test_doesnt_allow_nested_variables(self):
        bad_variable_fixtures = (
            'nested_dict_variables.yml',
            'nested_list_variables.yml',
        )
        for bad_variable_fixture in bad_variable_fixtures:
            try:
                prefs = load_prefs(_fixture_path(bad_variable_fixture))
            except APIBuddyException as err:
                assert 'variable' in err.title
                assert 'nested' in err.message
            else:
                assert False, f'{LOADED_MSG}{prefs}'

    def test_doesnt_allow_bools(self):
        bool_variable_fixtures = (
            'bool_variable_value.yml',
            'bool_variable_name.yml',
        )
        for bool_variable_fixture in bool_variable_fixtures:
            try:
                prefs = load_prefs(_fixture_path(bool_variable_fixture))
            except APIBuddyException as err:
                assert 'boolean' in err.title
                assert '\'true\'' in err.message  # helpful suggestion
            else:
                assert False, f'{LOADED_MSG}{prefs}'

    def test_doesnt_allow_special_characters(self):
        try:
            prefs = load_prefs(_fixture_path(
                'special_chars_variable_name.yml'
            ))
        except APIBuddyException as err:
            assert 'my_#{bad}_variable' in err.title
            assert 'special characters' in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_requires_known_oauth_type(self):
        try:
            prefs = load_prefs(_fixture_path(
                'oauth3.yml'
            ))
        except APIBuddyException as err:
            assert 'auth_type' in err.title
            assert 'should be one of these' in err.message
        else:
            assert False, f'{LOADED_MSG}{prefs}'

    def test_auth_type_can_be_none(self):
        prefs = load_prefs(_fixture_path(
            'no_auth.yml'
        ))
        assert prefs['auth_type'] is None


class TestSavePreferences(TempYAMLTestCase):
    def test_can_save_to_a_new_file(self):
        assert not path.isfile(TEMP_FILE)
        save_prefs(NEW_PREFS, TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        loaded_prefs = load_prefs(TEMP_FILE)
        assert loaded_prefs['api_url'] == NEW_PREFS['api_url']

    def test_doesnt_save_defaults_if_unchanged(self):
        assert not path.isfile(TEMP_FILE)
        save_prefs(NEW_PREFS, TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        with open(TEMP_FILE, 'r') as prefs_file:
            written_prefs = yaml.load(prefs_file)
        assert 'auth_test_status' not in written_prefs
        assert 'state' not in written_prefs['oauth2']
