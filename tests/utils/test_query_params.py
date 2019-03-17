from unittest import TestCase
from api_buddy.utils.http import pack_query_params, unpack_query_params
from api_buddy.utils.exceptions import APIBuddyException

FIRST_NAME = 'George'
MIDDLE_NAME = 'Louis'
LAST_NAME = 'Costanza'


class TestPackParams(TestCase):
    def test_parses_params_into_a_dict(self):
        packed_params = pack_query_params([
            f'first_name={FIRST_NAME}',
            f'last_name={LAST_NAME}',
        ])
        assert packed_params == {
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        }

    def test_when_not_provided_it_uses_an_empty_dict(self):
        assert pack_query_params([]) == {}

    def test_when_a_key_is_reused_it_becomes_a_list(self):
        packed_params = pack_query_params([
            f'names={FIRST_NAME}',
            f'names={MIDDLE_NAME}',
            f'names={LAST_NAME}',
        ])
        assert packed_params == {
            'names': [FIRST_NAME, MIDDLE_NAME, LAST_NAME]
        }

    def test_requires_exaclty_one_equals_sign_per_param(self):
        bad_params = ('key=val=other_val', 'keyval')
        for bad_param in bad_params:
            try:
                pack_query_params([bad_param])
            except APIBuddyException as err:
                assert 'param' in err.title
                assert bad_param in err.message
            else:
                assert False, f'{bad_param} was loaded'


class TestUnpackParams(TestCase):
    def test_parses_dict_into_a_list(self):
        packed_params = unpack_query_params({
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        })
        assert packed_params == [
            f'first_name={FIRST_NAME}',
            f'last_name={LAST_NAME}',
        ]

    def test_when_empty_it_returns_an_empty_list(self):
        assert unpack_query_params({}) == []

    def test_when_a_key_is_reused_it_becomes_multiple_entries(self):
        packed_params = unpack_query_params({
            'names': [FIRST_NAME, MIDDLE_NAME, LAST_NAME]
        })
        assert packed_params == [
            f'names={FIRST_NAME}',
            f'names={MIDDLE_NAME}',
            f'names={LAST_NAME}',
        ]
