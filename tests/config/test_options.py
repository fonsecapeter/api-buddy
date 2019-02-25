"""Testing validation only because testing docopt is hard + unnecessary"""
from copy import deepcopy
from unittest import TestCase
from api_buddy.typing import Options
from api_buddy.exceptions import APIBuddyException
from api_buddy.validation.options import validate_options
from api_buddy.utils import GET
from ..helpers import FAKE_ENDPOINT

FIRST_NAME = 'Cosmo'
MIDDLE_NAME = 'Van Nostrand'
LAST_NAME = 'Kramer'
RAW_OPTIONS: Options = {
    '<endpoint>': FAKE_ENDPOINT,
    '<params>': [],
    'get': True,
    'post': False,
    'patch': False,
    'put': False,
    'delete': False,
    '--help': False,
    '--version': False,
}


class TestLoadOptions(TestCase):
    def test_wont_allow_full_path_for_endpoint(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['<endpoint>'] = 'https://thecatapi.com/cats'
        try:
            validate_options(opts)
        except APIBuddyException as err:
            assert 'endpoint' in err.title
            # helpful suggestion
            assert 'cats' in err.message
        else:
            assert False

    def test_when_no_method_specified_it_uses_get(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        valid_opts = validate_options(opts)
        assert valid_opts['method'] == GET

    def test_when_method_is_specified_it_saves_as_enum(self):
        opts = deepcopy(RAW_OPTIONS)
        opts['get'] = False
        opts['post'] = True
        valid_opts = validate_options(opts)
        assert valid_opts['method'] == 'post'

    def test_if_multiple_methods_ever_get_selected_it_explodes(self):
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

    def test_when_params_are_not_provided_it_uses_an_empty_dict(self):
        opts = deepcopy(RAW_OPTIONS)
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {}

    def test_when_params_are_provided_it_parses_them_into_a_dict(self):
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

    def test_when_a_param_key_is_reused_it_becomes_a_list(self):
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
                assert False
