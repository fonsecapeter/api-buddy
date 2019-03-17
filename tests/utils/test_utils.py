from unittest import TestCase
from api_buddy.utils import api_url_join, format_dict_like_thing
from ..helpers import FAKE_API_URL, FAKE_API_VERSION, FAKE_ENDPOINT

NAME = 'Cosmo Kramer'
ALIAS = 'Dr. Martin Van Nostrand'
OCCUPATIONS = [
    'Bagelrista',
    'Car Parker',
    'Dermatologist',
]


class TestApiURLJoin(TestCase):
    def test_api_version_can_be_none(self):
        url = api_url_join(
            FAKE_API_URL,
            None,
            FAKE_ENDPOINT,
        )
        assert url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}'

    def test_it_includes_api_version(self):
        url = api_url_join(
            FAKE_API_URL,
            FAKE_API_VERSION,
            FAKE_ENDPOINT,
        )
        assert url == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}'

    def test_when_api_version_is_none_its_cool_about_slashes(self):
        url = api_url_join(
            f'{FAKE_API_URL}/',
            None,
            f'{FAKE_ENDPOINT}/',
        )
        assert url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}/'

    def test_when_api_version_is_included_its_still_cool_about_slashes(self):
        url = api_url_join(
            f'{FAKE_API_URL}/',
            f'{FAKE_API_VERSION}/',
            f'{FAKE_ENDPOINT}/',
        )
        assert url == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}/'


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
