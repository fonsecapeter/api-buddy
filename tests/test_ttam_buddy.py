from unittest import TestCase
from api_buddy.constants import VERSION


class TestAPIBuddy(TestCase):
    def test_has_a_version(self) -> None:
        versions = VERSION.split('.')
        assert len(versions) == 3
        for version in versions:
            int(version)
