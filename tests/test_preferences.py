from os import path
from pytest import raises
from unittest import TestCase
from ttam_buddy.preferences import load_prefs, EXAMPLE_PREFS
from ttam_buddy.constants import ROOT_DIR


class TestPreferences(TestCase):
    FIXTURES_DIR = path.join(ROOT_DIR, 'tests', 'fixtures')

    def test_can_load_from_a_yaml_file(self) -> None:
        prefs = load_prefs(
            path.join(self.FIXTURES_DIR, 'nonsense.yml')
        )
        assert prefs['banana'] is True
        assert prefs['something'] == 'yass queen'
        assert prefs['number'] == 7

    def test_has_defaults(self) -> None:
        prefs = load_prefs()
        assert prefs['account_id'] == 'demo_account_id'
        assert prefs['profile_id'] == 'demo_profile_id'

    def test_has_examples(self) -> None:
        assert 'client_id' in EXAMPLE_PREFS

    def test_merges_yaml_with_defaults(self) -> None:
        prefs = load_prefs(
            path.join(self.FIXTURES_DIR, 'test.yml')
        )
        assert prefs['client_id'] == 'my_favorite_client_id'
        assert prefs['client_secret'] == 'my_favorite_client_secret'
        assert prefs['account_id'] == 'demo_account_id'
        assert prefs['profile_id'] == 'demo_profile_id'

    def test_will_use_defaults_with_nonexistent_file_name(self) -> None:
        prefs = load_prefs(
            path.join(self.FIXTURES_DIR, 'doesnt_exist.yml')
        )
        assert prefs['account_id'] == 'demo_account_id'
        assert prefs['profile_id'] == 'demo_profile_id'

    def test_will_exit_with_bad_yaml(self) -> None:
        with raises(SystemExit) as pytest_wrapped_e:
            load_prefs(
                path.join(self.FIXTURES_DIR, 'bad.yml')
            )
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
