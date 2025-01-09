from unittest import TestCase
from api_buddy.utils.formatting import format_dict_like_thing
from api_buddy.config.themes import SHELLECTRIC

NAME = 'George Costanza'
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
            '  alias: Art Vandalay\n'
            '  name: George Costanza'
        )
        assert expected in format_dict_like_thing('', thing)

    def test_formats_list_values_as_multiliners(self):
        thing = {
            'name': NAME,
            'occupations': OCCUPATIONS,
        }
        expected = (
            '  name: George Costanza\n'
            '  occupations: \n'
            '    - Industrial smoother\n'
            '    - Architect\n'
            '    - Marine Biologist'
        )
        assert expected in format_dict_like_thing('', thing)

    def test_can_indent(self):
        thing = {
            'name': NAME,
            'occupations': OCCUPATIONS,
        }
        expected = (
            '    name: George Costanza\n'
            '    occupations: \n'
            '        - Industrial smoother\n'
            '        - Architect\n'
            '        - Marine Biologist'
        )
        assert expected in format_dict_like_thing('', thing, indent=4)

    def test_requires_a_name(self):
        assert 'Thing:' in format_dict_like_thing('Thing', {})

    def test_can_colorize(self):
        thing = {
            'alias': ALIAS,
            'name': NAME,
        }
        formatted = format_dict_like_thing('', thing, theme=SHELLECTRIC)
        assert 'alias' in formatted
        assert 'name' in formatted
        for value in [ALIAS, NAME]:
            for word in value:
                assert word in formatted
