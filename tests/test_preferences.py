import yaml
from os import path, remove
from pytest import raises
from unittest import TestCase
from ttam_buddy.preferences import (
    DEFAULT_PREFS,
    EXAMPLE_PREFS,
    DEFAULT_KEYS_TO_KEEP,
    Preferences,
    load_prefs,
    save_prefs,
)
from ttam_buddy.constants import ROOT_DIR

FIXTURES_DIR = path.join(ROOT_DIR, 'tests', 'fixtures')
TEMP_FILE = path.join(FIXTURES_DIR, 'temp.yml')
TEST_PREFS: Preferences = {
    'api_url': 'https://thecatapi.com/',
    'client_id': 'mittens',
    'client_secret': 'whiskers',
    'scopes': ['fails', 'stuck_in_boxes'],
    'redirect_uri': 'http://localhost:8080/',
    'auth_test_path': '/secret_cats',
    'access_token': 'feline_token',
    'state': None,
    'auth_test_status': 401,
}


def clean_temp_yml_file() -> None:
    if path.isfile(TEMP_FILE):
        remove(TEMP_FILE)


class TestLoadPreferences(TestCase):

    def setUp(self):
        clean_temp_yml_file()

    def tearDown(self):
        clean_temp_yml_file()

    def test_can_load_from_a_yaml_file(self):
        prefs = load_prefs(
            path.join(FIXTURES_DIR, 'nonsense.yml')
        )
        assert prefs['api_url'] == 'https://seinfeld-quotes.herokuapp.com/'
        assert prefs['scopes'] == ['quotes', 'episodes']
        assert prefs['state'] is None
        assert prefs['auth_test_status'] == 403

    def test_has_defaults(self):
        prefs = load_prefs()
        assert prefs == DEFAULT_PREFS

    def test_merges_yaml_with_defaults(self):
        prefs = load_prefs(
            path.join(FIXTURES_DIR, 'test.yml')
        )
        assert prefs['client_id'] == 'my_favorite_client_id'
        assert prefs['client_secret'] == 'my_favorite_client_secret'
        assert prefs['redirect_uri'] == DEFAULT_PREFS['redirect_uri']

    def test_when_file_doesnt_exist_it_writes_example_prefs(self):
        assert not path.isfile(TEMP_FILE)
        prefs = load_prefs(TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        for key, example_val in EXAMPLE_PREFS.items():
            assert prefs[key] == example_val

    def test_when_yaml_is_invalid_it_will_exit(self):
        with raises(SystemExit) as pytest_wrapped_e:
            load_prefs(
                path.join(FIXTURES_DIR, 'bad.yml')
            )
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


class TestSavePreferences(TestCase):

    def setUp(self):
        clean_temp_yml_file()

    def tearDown(self):
        clean_temp_yml_file()

    def test_can_save_to_a_new_file(self):
        assert not path.isfile(TEMP_FILE)
        save_prefs(TEST_PREFS, TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        loaded_prefs = load_prefs(TEMP_FILE)
        assert loaded_prefs['api_url'] == TEST_PREFS['api_url']

    def test_doesnt_save_defaults_if_unchanged(self):
        assert not path.isfile(TEMP_FILE)
        save_prefs(TEST_PREFS, TEMP_FILE)
        assert path.isfile(TEMP_FILE)
        with open(TEMP_FILE, 'r') as prefs_file:
            written_prefs = yaml.load(prefs_file)
        for key in ('state', 'auth_test_status'):
            assert key not in written_prefs
