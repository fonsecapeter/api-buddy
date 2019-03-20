from unittest import TestCase
from api_buddy.utils.formatting import format_dict_like_thing
from api_buddy.config.themes import SHELLECTRIC

NAME = 'Goerge Costanza'
ALIAS = 'Art Vandalay'
OCCUPATIONS = [
    'Industrial smoother',
    'Architect',
    'Marine Biologist',
]


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

    def test_can_colorize(self):
        thing = {
            'alias': ALIAS,
            'name': NAME,
        }
        formatted = format_dict_like_thing('', thing, SHELLECTRIC)
        assert 'alias' in formatted
        assert ALIAS in formatted
        assert 'name' in formatted
        assert NAME in formatted
