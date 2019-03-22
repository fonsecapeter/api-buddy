from unittest import TestCase
from api_buddy.utils.exceptions import APIBuddyException
from api_buddy.utils.formatting import flat_str_dict


NAME = 'Cosmo Kramer'
ALIAS = 'Dr. Martin Van Nostrand'
OCCUPATIONS = [
    'Bagelrista',
    'Car Parker',
    'Dermatologist',
]


class FlatStrDict(TestCase):
    def test_converts_things_to_strings(self):
        converted = flat_str_dict(':D', {
            'simple_str': 'is most common',
            'ints': 2,
            3: 3,
        })
        assert converted == {
            'simple_str': 'is most common',
            'ints': '2',
            '3': '3',  # keys are stringified too
        }

    def test_doesnt_allow_nesting(self):
        bad_things = (
            {'nested_list': [
                'chunky',
                'monkey',
            ]},
            {'nested_dict': {
                'aint': 'gonna',
                'fly': 'here',
            }},
        )
        for bad_thing in bad_things:
            try:
                converted = flat_str_dict(':O', bad_thing)
            except APIBuddyException as err:
                assert 'nested' in err.message
            else:
                assert False, f'Converted just fine: {converted}'

    def test_doesnt_allow_booleans(self):
        bad_things = (
            {'true': True},
            {True: 'true'},
        )
        for bad_thing in bad_things:
            try:
                converted = flat_str_dict(':U', bad_thing)
            except APIBuddyException as err:
                assert 'boolean' in err.title
                assert '\'true\'' in err.message  # helpful suggestion
            else:
                assert False, f'Converted just fine: {converted}'

    def test_doesnt_allow_null_keys(self):
        try:
            converted = flat_str_dict(':o', {None: 'porque'})
        except APIBuddyException as err:
            assert 'null' in err.message
        else:
            assert False, f'Converted just fine: {converted}'

    def test_can_check_for_variable_interpolation_chars(self):
        try:
            converted = flat_str_dict(':|', {
                'my_#{bad}_variable': 'why would anyone do this',
            }, check_special_chars=True)
        except APIBuddyException as err:
            assert 'my_#{bad}_variable' in err.title
            assert 'special characters' in err.message
        else:
            assert False, f'Converted just fine: {converted}'

    def test_uses_custom_name_in_errors(self):
        name = 'hello'
        try:
            converted = flat_str_dict(name, {True: True})
        except APIBuddyException as err:
            assert name in err.title
        else:
            assert False, f'Converted just fine: {converted}'
