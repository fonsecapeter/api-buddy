"""Testing validation only because testing docopt is hard + unnecessary"""
from copy import deepcopy
from unittest import TestCase
from api_buddy.utils.typing import RawOptions
from api_buddy.utils.exceptions import APIBuddyException
from api_buddy.validation.options import validate_options
from api_buddy.utils.http import GET
from ..helpers import FAKE_ENDPOINT

FIRST_NAME = 'Cosmo'
MIDDLE_NAME = 'Van Nostrand'
LAST_NAME = 'Kramer'
RAW_OPTIONS: RawOptions = {
    '<endpoint>': FAKE_ENDPOINT,
    '<params>': [],
    '<data>': None,
    '<api_url>': None,
    'get': True,
    'post': False,
    'patch': False,
    'put': False,
    'delete': False,
    'help': False,
    '--help': False,
    '--version': False,
}


class TestEndpoint(TestCase):
    def test_if_contains_scheme_will_split_out_opts_api_url(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['<endpoint>'] = 'https://thecatapi.com/cats'
        valid_opts = validate_options(opts)
        assert valid_opts['<api_url>'] == 'https://thecatapi.com'
        assert valid_opts['<endpoint>'] == '/cats'


class TestMethod(TestCase):
    def test_when_not_specified_it_uses_get(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        valid_opts = validate_options(opts)
        assert valid_opts['<method>'] == GET

    def test_when_specified_it_saves_as_enum(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        opts['post'] = True
        valid_opts = validate_options(opts)
        assert valid_opts['<method>'] == 'post'

    def test_if_multiple_are_specified_it_explodes(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['post'] = True
        opts['delete'] = True
        try:
            validate_options(opts)
        except APIBuddyException as err:
            assert 'methods' in err.title
            assert 'more than one method' in err.message
        else:
            assert False


class TestParams(TestCase):
    def test_parses_params_into_a_dict(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['<params>'] = [
            f'first_name={FIRST_NAME}',
            f'last_name={LAST_NAME}',
        ]
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        }

    def test_when_not_provided_it_uses_an_empty_dict(self):
        opts = deepcopy(RAW_OPTIONS)
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {}

    def test_when_a_key_is_reused_it_becomes_a_list(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['<params>'] = [
            f'names={FIRST_NAME}',
            f'names={MIDDLE_NAME}',
            f'names={LAST_NAME}',
        ]
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {
            'names': [FIRST_NAME, MIDDLE_NAME, LAST_NAME]
        }

    def test_requires_exaclty_one_equals_sign_per_param(self):
        bad_params = ('key=val=other_val', 'keyval')
        for bad_param in bad_params:
            opts = deepcopy(RAW_OPTIONS)
            opts['<params>'] = [bad_param]
            try:
                validate_options(opts)
            except APIBuddyException as err:
                assert 'param' in err.title
                assert bad_param in err.message
            else:
                assert False, f'{bad_param} was loaded'


class TestData(TestCase):
    def test_when_there_are_no_params_it_finds_the_data(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        opts['post'] = True
        opts['<params>'] = [f'{{"first_name": "{FIRST_NAME}"}}']
        valid_opts = validate_options(opts)
        assert valid_opts['<data>'] == {'first_name': FIRST_NAME}
        assert valid_opts['<params>'] == {}

    def test_when_there_are_params_it_finds_the_data(self):
        param = f'first_name={FIRST_NAME}'
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        opts['post'] = True
        opts['<params>'] = [
            param,
            f'{{"last_name": "{LAST_NAME}"}}',
        ]
        valid_opts = validate_options(opts)
        assert valid_opts['<data>'] == {'last_name': LAST_NAME}
        assert valid_opts['<params>'] == {'first_name': FIRST_NAME}

    def test_can_load_all_kinds_of_json(self):
        data = {
            '{"compact":true}': {'compact': True},
            '{"spaces": "around", "separators": true}': {
                'spaces': 'around',
                'separators': True,
            },
            '''{
              "indenting": "Of any kind",
              "works": "🙌"
            }''': {
                'indenting': 'Of any kind',
                'works': '🙌',
            },
            '["lists", "are", "cool", 2]': [
                'lists',
                'are',
                'cool',
                2,
            ],
        }
        for json_str, python_obj in data.items():
            opts = deepcopy(RAW_OPTIONS)
            opts['get'] = False
            opts['post'] = True
            opts['<params>'] = [json_str]
            valid_opts = validate_options(opts)
            assert valid_opts['<data>'] == python_obj

    def test_defaults_to_none(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        opts['post'] = True
        valid_opts = validate_options(opts)
        assert valid_opts['<data>'] is None

    def test_data_must_be_valid_json(self):
        bad_data = [
            '{"mising":"closing_bracket"',
            '{correctly_quoted: false}',
            '["list" "without" "commas"]',
            '[anything,with,trailing,commas,]',
        ]
        for bad_datum in bad_data:
            opts = deepcopy(RAW_OPTIONS)
            opts['get'] = False
            opts['post'] = True
            opts['<params>'] = [bad_datum]
            try:
                validate_options(opts)
            except APIBuddyException as err:
                assert 'request body data' in err.title
                assert 'valid json' in err.message
            else:
                assert False, f'{bad_datum} was loaded'

    def test_when_method_is_get_data_isnt_allowed(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['<params>'] = [f'{{"first_name": "{FIRST_NAME}"}}']
        try:
            validate_options(opts)
        except APIBuddyException as err:
            assert 'data with' in err.title
            assert 'GET' in err.title
            assert 'Did you mean' in err.message
            assert 'POST' in err.message
        else:
            assert False
