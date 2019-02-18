"""Testing validation only because testing docopt is hard + unnecessary"""
from unittest import TestCase
from api_buddy.exceptions import APIBuddyException
from api_buddy.validation.options import validate_options


class TestLoadPreferences(TestCase):
    def test_wont_allow_full_path_for_endpoint(self):
        opts = {
            '<endpoint>': 'https://thecatapi.com/cats',
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

    def test_when_no_method_specified_it_uses_get(self):
        opts = {
            '<endpoint>': '/cats',
            'get': False,
            '--help': False,
            '--version': False,
        }
        valid_opts = validate_options(opts)
        assert valid_opts['get'] is True
