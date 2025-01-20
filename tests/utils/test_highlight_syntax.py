from unittest import TestCase
from api_buddy.config.themes import SHELLECTRIC
from api_buddy.utils.formatting import YAML, highlight_syntax


NAME = "Elaine"
ALIAS = "Laney"
OCCUPATIONS = [
    "Writer",
    "Assistant",
    "Shut Up!",
]
JSON_THING = (
    "{\n"
    f'  "name": "{NAME}",\n'
    f'  "alias": "{ALIAS}",\n'
    '  "occupations": [\n'
    f'    "{OCCUPATIONS[0]}",\n'
    f'    "{OCCUPATIONS[1]}",\n'
    f'    "{OCCUPATIONS[2]}",\n'
    "  ],\n"
    f'  "is_cool": true\n'
    "}"
)
SHELLECTRIC_JSON_THING = (
    "\x1b[37m{\x1b[39m\n\x1b[95m  "
    '\x1b[39m\x1b[33m"name"\x1b[39m\x1b[37m:\x1b[39m\x1b[95m '
    '\x1b[39m\x1b[91m"Elaine"\x1b[39m\x1b[37m,\x1b[39m\n\x1b[95m  '
    '\x1b[39m\x1b[33m"alias"\x1b[39m\x1b[37m:\x1b[39m\x1b[95m '
    '\x1b[39m\x1b[91m"Laney"\x1b[39m\x1b[37m,\x1b[39m\n\x1b[95m  '
    '\x1b[39m\x1b[33m"occupations"\x1b[39m\x1b[37m:\x1b[39m\x1b[95m '
    "\x1b[39m\x1b[37m[\x1b[39m\n\x1b[95m    "
    '\x1b[39m\x1b[91m"Writer"\x1b[39m\x1b[37m,\x1b[39m\n\x1b[95m    '
    '\x1b[39m\x1b[91m"Assistant"\x1b[39m\x1b[37m,\x1b[39m\n\x1b[95m    '
    '\x1b[39m\x1b[91m"Shut Up!"\x1b[39m\x1b[37m,\x1b[39m\n\x1b[95m  '
    "\x1b[39m\x1b[37m],\x1b[39m\n\x1b[95m  "
    '\x1b[39m\x1b[33m"is_cool"\x1b[39m\x1b[37m:\x1b[39m\x1b[95m '
    "\x1b[39m\x1b[96mtrue\x1b[39m\n\x1b[37m}\x1b[39m\n"
)
YAML_THING = (
    f"name: {NAME},\n"
    f"alias: {ALIAS},\n"
    'occupations":\n'
    f"  - {OCCUPATIONS[0]},\n"
    f"  - {OCCUPATIONS[1]},\n"
    f"  - {OCCUPATIONS[2]},\n"
    f"is_cool: true\n"
)


class TestHighlightSyntax(TestCase):
    def _assert_things_are_still_there(self, highlighted: str) -> None:
        for value in [NAME, ALIAS] + OCCUPATIONS:
            for word in value.split(" "):
                assert word in highlighted

    def test_can_highglight_json(self):
        highlighted = highlight_syntax(JSON_THING, SHELLECTRIC)
        assert highlighted == SHELLECTRIC_JSON_THING

    def test_can_highglight_yaml(self):
        highlighted = highlight_syntax(YAML_THING, SHELLECTRIC, lang=YAML)
        self._assert_things_are_still_there(highlighted)

    def test_can_use_pygments_themes(self):
        some_themes = ("monokai", "emacs", "arduino", "paraiso-dark")
        for theme in some_themes:
            highlighted = highlight_syntax(JSON_THING, theme)
            self._assert_things_are_still_there(highlighted)
            assert highlighted != SHELLECTRIC_JSON_THING

    def test_can_use_no_theme(self):
        highlighted = highlight_syntax(JSON_THING, None)
        assert highlighted == JSON_THING
