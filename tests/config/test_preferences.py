import yaml
from os import path
from api_buddy.exceptions import APIBuddyException
from api_buddy.typing import Preferences
from api_buddy.validation.preferences import DEFAULT_PREFS
from api_buddy.config.preferences import (
    EXAMPLE_PREFS,
    load_prefs,
    save_prefs,
)
from ..helpers import (
    FIXTURES_DIR,
    TEMP_FILE,
    TempYAMLTestCase,
)


CAT_FACTS_API_URL = 'https://alexwohlbruck.github.io/cat-facts'
NEW_PREFS: Preferences = {
    'api_url': 'https://thecatapi.com',
    'client_id': 'mittens',
    'client_secret': 'whiskers',
    'scopes': ['fails', 'stuck_in_boxes'],
    'redirect_uri': 'http://localhost:8080/',
    'access_token': 'feline_token',
    'state': None,
    'auth_test_status': 401,
    'api_version': None,
}


def _fixture_path(file_name):
    abs_path = path.join(FIXTURES_DIR, file_name)
    assert path.isfile(abs_path)
    return abs_path


class TestLoadPreferences(TempYAMLTestCase):
    def test_can_load_from_a_yaml_file(self):
        prefs = load_prefs(_fixture_path('test.yml'))
        assert prefs['api_url'] == 'https://seinfeld-quotes.herokuapp.com'
        assert prefs['client_id'] == 'my_favorite_client_id'
        assert prefs['client_secret'] == 'my_favorite_client_secret'
        assert prefs['scopes'] == ['quotes', 'episodes']
        assert prefs['state'] is None
        assert prefs['auth_test_status'] == 403

    def test_merges_yaml_with_defaults(self):
        prefs = load_prefs(_fixture_path('test.yml'))
        assert prefs['client_id'] == 'my_favorite_client_id'     # retains non-default
        assert prefs['redirect_uri'] == DEFAULT_PREFS['redirect_uri']  # not specified
        assert prefs['api_version'] == DEFAULT_PREFS['api_version']  # not specified
        assert prefs['auth_test_status'] == 403                  # overwritten default

    def test_when_file_doesnt_exist_it_writes_example_prefs(self):
        assert not path.isfile(TEMP_FILE)
        prefs = load_prefs(TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        for key, example_val in EXAMPLE_PREFS.items():
            assert prefs[key] == example_val

    def test_file_must_contain_valid_yaml(self):
        try:
            load_prefs(_fixture_path('bad.yml'))
        except APIBuddyException as err:
            assert 'problem reading' in err.title
            assert 'valid yaml' in err.message
        else:
            assert False

    def test_file_cant_be_empty(self):
        try:
            load_prefs(_fixture_path('empty.yml'))
        except APIBuddyException as err:
            assert 'preferences are empty' in err.title
            assert f'client_id: {EXAMPLE_PREFS["client_id"]}' in err.message
        else:
            assert False

    def test_validates_field_types(self):
        try:
            load_prefs(_fixture_path('bad_types.yml'))
        except APIBuddyException as err:
            assert 'preferences are funky' in err.title
            assert 'client_id' in err.message
        else:
            assert False

    def test_validates_required_fields(self):
        try:
            load_prefs(_fixture_path('missing_fields.yml'))
        except APIBuddyException as err:
            assert 'preferences are funky' in err.title
            assert 'api_url' in err.message
            assert 'client_secret' in err.message
        else:
            assert False

    def test_adds_default_api_url_scheme_if_missing(self):
        prefs = load_prefs(_fixture_path('api_url_without_scheme.yml'))
        assert prefs['api_url'] == CAT_FACTS_API_URL

    def test_doesnt_allow_query_string_in_api_url(self):
        try:
            load_prefs(_fixture_path('api_url_with_query_string.yml'))
        except APIBuddyException as err:
            assert 'query parameters' in err.title
            # helpful suggestion
            assert CAT_FACTS_API_URL in err.message
        else:
            assert False

    def test_doesnt_allow_hash_fragments_in_api_url(self):
        try:
            load_prefs(_fixture_path('api_url_with_hash_fragment.yml'))
        except APIBuddyException as err:
            assert 'hash fragments' in err.title
            # helpful suggestion
            assert CAT_FACTS_API_URL in err.message
        else:
            assert False

    def test_supports_string_api_versions(self):
        prefs = load_prefs(_fixture_path('api_version_as_str.yml'))
        assert prefs['api_version'] == 'three'

    def test_when_api_version_is_not_none_it_coerces_to_str(self):
        prefs = load_prefs(_fixture_path('api_version_as_int.yml'))
        assert prefs['api_version'] == '3'


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
        for key in ('state', 'auth_test_status'):
            assert key not in written_prefs
