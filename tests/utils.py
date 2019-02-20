from unittest import TestCase
from api_buddy.utils import api_url_join
from .helpers import FAKE_API_URL, FAKE_API_VERSION, FAKE_ENDPOINT


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
        assert url == f'{FAKE_API_URL}/{FAKE_ENDPOINT}'

    def test_when_api_version_is_included_its_still_cool_about_slashes(self):
        url = api_url_join(
            f'{FAKE_API_URL}/',
            f'{FAKE_API_VERSION}/',
            f'{FAKE_ENDPOINT}/',
        )
        assert url == f'{FAKE_API_URL}/{FAKE_API_VERSION}/{FAKE_ENDPOINT}'
