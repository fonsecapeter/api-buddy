from copy import deepcopy
from unittest import TestCase

from api_buddy.config.variables import interpolate_variables
from tests.helpers import TEST_OPTIONS, TEST_PREFERENCES

NAME = "art_vandalay"
OCCUPATION = "marine_biologist"
VARIABLES = {
    "name": NAME,
    "occupation": OCCUPATION,
}


class TestVariables(TestCase):
    def setUp(self):
        self.opts = deepcopy(TEST_OPTIONS)
        self.prefs = deepcopy(TEST_PREFERENCES)
        self.prefs["variables"] = VARIABLES

    def test_can_interpolate_endpoint(self):
        self.opts["<endpoint>"] = "/employees/#{occupation}/#{name}"
        opts = interpolate_variables(self.opts, self.prefs)
        assert opts["<endpoint>"] == f"/employees/{OCCUPATION}/{NAME}"

    def test_can_interpolate_singular_params(self):
        self.opts["<params>"] = {
            "name": "sir_#{name}",
            "occupation": "#{occupation}",
        }
        opts = interpolate_variables(self.opts, self.prefs)
        assert opts["<params>"] == {
            "name": f"sir_{NAME}",
            "occupation": OCCUPATION,
        }

    def test_can_interpolate_plural_params(self):
        self.opts["<params>"] = {
            "name": ["#{name}", "#{occupation}"],
        }
        opts = interpolate_variables(self.opts, self.prefs)
        assert opts["<params>"] == {
            "name": [NAME, OCCUPATION],
        }

    def test_can_interpolate_data(self):
        self.opts["<data>"] = {
            "name": "#{name}",
            "#{occupation}": "occupation",
        }
        opts = interpolate_variables(self.opts, self.prefs)
        assert opts["<data>"] == {
            "name": NAME,
            OCCUPATION: "occupation",
        }
