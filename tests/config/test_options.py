"""Testing validation only because testing docopt is hard + unnecessary"""
from unittest import TestCase
from api_buddy.exceptions import APIBuddyException
from api_buddy.validation.options import validate_options

FIRST_NAME = 'Cosmo'
MIDDLE_NAME = 'Van Nostrand'
LAST_NAME = 'Kramer'


class TestLoadOptions(TestCase):
    def test_wont_allow_full_path_for_endpoint(self):
        opts = {
            '<endpoint>': 'https://thecatapi.com/cats',
            '<params>': [],
            'get': True,
            '--help': False,
            '--version': False,
        }
        try:
            validate_options(opts)
        except APIBuddyException as err:
            assert 'endpoint' in err.title
            # helpful suggestion
            assert 'cats' in err.message
        else:
            assert False

    def test_when_no_method_specified_it_uses_get(self):
        opts = {
            '<endpoint>': '/cats',
            '<params>': [],
            'get': False,
            '--help': False,
            '--version': False,
        }
        valid_opts = validate_options(opts)
        assert valid_opts['get'] is True

    def test_when_params_are_provided_it_parses_them_into_a_dict(self):
        opts = {
            '<endpoint>': '/cats',
            '<params>': [
                f'first_name={FIRST_NAME}',
                f'last_name={LAST_NAME}',
            ],
            'get': False,
            '--help': False,
            '--version': False,
        }
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        }

    def test_when_a_param_key_is_reused_it_becomes_a_list(self):
        opts = {
            '<endpoint>': '/cats',
            '<params>': [
                f'names={FIRST_NAME}',
                f'names={MIDDLE_NAME}',
                f'names={LAST_NAME}',
            ],
            'get': False,
            '--help': False,
            '--version': False,
        }
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {
            'names': [FIRST_NAME, MIDDLE_NAME, LAST_NAME]
        }

    def test_when_params_are_not_provided_it_uses_an_empty_dict(self):
        opts = {
            '<endpoint>': '/cats',
            '<params>': [],
            'get': False,
            '--help': False,
            '--version': False,
        }
        valid_opts = validate_options(opts)
        assert valid_opts['<params>'] == {}

    def test_requires_exaclty_one_equals_sign_per_param(self):
        bad_params = ('key=val=other_val', 'keyval')
        for bad_param in bad_params:
            opts = {
                '<endpoint>': '/cats',
                '<params>': [bad_param],
                'get': False,
                '--help': False,
                '--version': False,
            }
            try:
                validate_options(opts)
            except APIBuddyException as err:
                assert 'param' in err.title
                assert bad_param in err.message
            else:
                assert False
