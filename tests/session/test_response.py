from mock import MagicMock, PropertyMock
from unittest import TestCase
from api_buddy.session.response import format_response

TEXT_TO_KEEP = 'This text should stay'

class TestFormatResponse(TestCase):
    def test_when_json_it_can_expand_and_indent(self):
        resp = MagicMock()
        resp.json.return_value = {'it': 'works'}
        formatted = format_response(resp)
        assert formatted == '{\n  "it": "works"\n}'

    def test_when_html_it_can_strip_tags(self):
        resp = MagicMock()
        type(resp).text = PropertyMock(return_value=(
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
        formatted = format_response(resp)
        assert formatted == (
            f'{TEXT_TO_KEEP}\n'
            f'{TEXT_TO_KEEP}'
        )

    def test_falls_back_to_unformatted_text(self):
        resp = MagicMock()
        type(resp).text = PropertyMock(
            return_value=TEXT_TO_KEEP
        )
        formatted = format_response(resp)
        assert formatted == TEXT_TO_KEEP
