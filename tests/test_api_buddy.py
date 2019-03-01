from unittest import TestCase
from api_buddy.utils import VERSION


class TestAPIBuddy(TestCase):
    def test_has_a_version(self) -> None:
        versions = VERSION.split('.')
        assert len(versions) == 3
        for version in versions:
            int(version)
