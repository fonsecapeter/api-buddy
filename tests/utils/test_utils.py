from unittest import TestCase
from api_buddy.utils import (
    api_url_join,
    format_dict_like_thing,
    flat_str_dict,
    UtilException
)
from ..helpers import FAKE_API_URL, FAKE_API_VERSION, FAKE_ENDPOINT

NAME = 'Cosmo Kramer'
ALIAS = 'Dr. Martin Van Nostrand'
OCCUPATIONS = [
    'Bagelrista',
    'Car Parker',
    'Dermatologist',
]


class TestApiURLJoin(TestCase):
    def test_api_version_can_be_none(self):
        url = api_url_join(
            FAKE_API_URL,
            None,
            FAKE_ENDPOINT,
        )
        assert url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}'

    def test_it_includes_api_version(self):
        url = api_url_join(
            FAKE_API_URL,
            FAKE_API_VERSION,
            FAKE_ENDPOINT,
        )
        assert url == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}'

    def test_when_api_version_is_none_its_cool_about_slashes(self):
        url = api_url_join(
            f'{FAKE_API_URL}/',
            None,
            f'{FAKE_ENDPOINT}/',
        )
        assert url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}/'

    def test_when_api_version_is_included_its_still_cool_about_slashes(self):
        url = api_url_join(
            f'{FAKE_API_URL}/',
            f'{FAKE_API_VERSION}/',
            f'{FAKE_ENDPOINT}/',
        )
        assert url == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}/'


class TestFormatDictLikeThing(TestCase):
    def test_can_format_a_dict(self):
        thing = {
            'alias': ALIAS,
            'name': NAME,
        }
        expected = (
            f'  alias: {ALIAS}\n'
            f'  name: {NAME}'
        )
        assert expected in format_dict_like_thing('', thing)

    def test_formats_list_values_as_multiliners(self):
        thing = {
            'name': NAME,
            'occupations': OCCUPATIONS,
        }
        expected = (
            f'  name: {NAME}\n'
            f'  occupations: \n'
            f'    - {OCCUPATIONS[0]}\n'
            f'    - {OCCUPATIONS[1]}\n'
            f'    - {OCCUPATIONS[2]}'
        )
        assert expected in format_dict_like_thing('', thing)

    def test_requires_a_name(self):
        name = 'Thing'
        assert f'{name}:' in format_dict_like_thing(name, {})


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
            except UtilException as err:
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
            except UtilException as err:
                assert 'boolean' in err.title
                assert '\'true\'' in err.message  # helpful suggestion
            else:
                assert False, f'Converted just fine: {converted}'

    def test_doesnt_allow_null_keys(self):
        try:
            converted = flat_str_dict(':o', {None: 'porque'})
        except UtilException as err:
            assert 'null' in err.message
        else:
            assert False, f'Converted just fine: {converted}'

    def test_can_check_for_variable_interpolation_chars(self):
        try:
            converted = flat_str_dict(':|', {
                'my_#{bad}_variable': 'why would anyone do this',
            }, check_special_chars=True)
        except UtilException as err:
            assert 'my_#{bad}_variable' in err.title
            assert 'special characters' in err.message
        else:
            assert False, f'Converted just fine: {converted}'

    def test_uses_custom_name_in_errors(self):
        name = 'hello'
        try:
            converted = flat_str_dict(name, {True: True})
        except UtilException as err:
            assert name in err.title
        else:
            assert False, f'Converted just fine: {converted}'
