import unittest

from molgenis.capice.utilities.enums import Versioning
from src.molgenis.capice.__version__ import __version__
from re import match


class TestVersion(unittest.TestCase):
    def test_version_formatting(self):
        if match(Versioning.VALIDATION_REGEX.value, __version__) is None:
            raise ValueError('CAPICE has invalid version format')


if __name__ == '__main__':
    unittest.main()
