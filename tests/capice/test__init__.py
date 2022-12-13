import unittest
from re import match

from molgenis.capice.utilities.enums import Versioning
from molgenis.capice import __version__


class TestVersion(unittest.TestCase):
    def test_version_formatting(self):
        """
        Test that assures CAPICE is not given an invalid version number.
        """
        if match(Versioning.VALIDATION_REGEX.value, __version__) is None:
            raise ValueError('CAPICE has invalid version format')


if __name__ == '__main__':
    unittest.main()
