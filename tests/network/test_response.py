from copy import deepcopy
from mock import MagicMock, PropertyMock
from unittest import TestCase
from api_buddy.network.response import format_response, print_response
from api_buddy.config.themes import SHELLECTRIC
from ..helpers import TEST_PREFERENCES

TEXT_TO_KEEP = 'This text should stay'


class TestPrintResponse(TestCase):
    def setUp(self):
        self.prefs = deepcopy(TEST_PREFERENCES)
        self.resp = MagicMock()
        type(self.resp).headers = {'a': 'b'}
        type(self.resp).cookies = {'c': 'd'}

    def test_can_print_response(self):
        # should not raise any errors
        print_response(self.resp, self.prefs)

    def test_can_print_verbose_response(self):
        self.prefs['verboseness']['response'] = True
        # should not raise any errors
        print_response(self.resp, self.prefs)

    def test_can_prints_statuses(self):
        type(self.resp).ok = True
        # should not raise any errors
        print_response(self.resp, self.prefs)
        type(self.resp).ok = False
        # should not raise any errors
        print_response(self.resp, self.prefs)


class TestFormatResponse(TestCase):
    def setUp(self):
        self.resp = MagicMock()
        self.prefs = deepcopy(TEST_PREFERENCES)

    def test_when_json_it_can_expand_and_indent(self):
        self.resp.json.return_value = {'it': 'works'}
        formatted = format_response(self.resp, 2, None)
        assert formatted == '{\n  "it": "works"\n}'

    def test_can_style_json(self):
        self.resp.json.return_value = {'it': 'works'}
        formatted = format_response(self.resp, 2, SHELLECTRIC)
        assert '"it"' in formatted
        assert '"works"' in formatted

    def test_honors_indent(self):
        self.resp.json.return_value = {'it': 'works'}
        formatted = format_response(self.resp, 4, None)
        assert formatted == '{\n    "it": "works"\n}'
        formatted = format_response(self.resp, None, None)
        assert formatted == '{"it": "works"}'

    def test_when_html_it_can_strip_tags(self):
        type(self.resp).text = PropertyMock(return_value=(
            '<!DOCTYPE html>\n'
            '<html>\n'
            '  <head>\n'
            '    <meta charset="UTF-8">\n'
            '    <title>title</title>\n'
            '    <style>delete me!</style>\n'
            '    <script>me too!</script>\n'
            '  </head>\n'
            '  <body>\n'
            '    <header>ignore this</header>\n'
            '    <nav>and this</nav>\n'
            f'    <h1>{TEXT_TO_KEEP}</h1>\n'
            '    <a href="banana">\n'
            '      can argue this is not important either\n'
            '    </a>\n'
            f'    <p>{TEXT_TO_KEEP}</p>\n'
            '  </body>\n'
            '</html>\n'
        ))
        formatted = format_response(self.resp, None, None)
        assert formatted == (
            f'{TEXT_TO_KEEP}\n'
            f'{TEXT_TO_KEEP}'
        )

    def test_falls_back_to_unformatted_text(self):
        type(self.resp).text = PropertyMock(
            return_value=TEXT_TO_KEEP
        )
        formatted = format_response(self.resp, None, None)
        assert formatted == TEXT_TO_KEEP
