import unittest
from re import match
from importlib import metadata

from molgenis.capice.utilities.enums import Versioning


class TestVersion(unittest.TestCase):
    def test_version_formatting(self):
        """
        Test that assures CAPICE is not given an invalid version number.
        """
        if match(Versioning.VALIDATION_REGEX.value, metadata.version("capice")) is None:
            raise ValueError('CAPICE has invalid version format')


if __name__ == '__main__':
    unittest.main()
