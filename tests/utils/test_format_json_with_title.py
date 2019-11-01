from unittest import TestCase
from api_buddy.utils.formatting import format_json_with_title
from api_buddy.config.themes import SHELLECTRIC

NAME = 'George Costanza'
ALIAS = 'Art Vandalay'
OCCUPATIONS = [
    'Industrial smoother',
    'Architect',
    'Marine Biologist',
]


class TestFormatJSONWithTitle(TestCase):
    def test_can_format_json(self):
        thing = {
            'alias': ALIAS,
            'name': NAME,
            'occupations': OCCUPATIONS
        }
        expected = (
            'Thing:\n'
            '  {\n'
            '    "alias": "Art Vandalay",\n'
            '    "name": "George Costanza",\n'
            '    "occupations": [\n'
            '      "Industrial smoother",\n'
            '      "Architect",\n'
            '      "Marine Biologist"\n'
            '    ]\n'
            '  }'
        )
        assert expected == format_json_with_title('Thing', thing)

    def test_can_indent(self):
        thing = {
            'alias': ALIAS,
            'name': NAME,
            'occupations': OCCUPATIONS
        }
        expected = (
            'Thing:\n'
            '    {\n'
            '        "alias": "Art Vandalay",\n'
            '        "name": "George Costanza",\n'
            '        "occupations": [\n'
            '            "Industrial smoother",\n'
            '            "Architect",\n'
            '            "Marine Biologist"\n'
            '        ]\n'
            '    }'
        )
        assert expected == format_json_with_title('Thing', thing, indent=4)

    def test_can_use_no_indent(self):
        thing = {'name': NAME}
        expected = (
            'Thing:\n'
            '  {"name": "George Costanza"}'
        )
        assert expected == format_json_with_title('Thing', thing, indent=None)

    def test_can_colorize(self):
        thing = {
            'alias': ALIAS,
            'name': NAME,
        }
        formatted = format_json_with_title('', thing, theme=SHELLECTRIC)
        assert 'alias' in formatted
        assert ALIAS in formatted
        assert 'name' in formatted
        assert NAME in formatted
