import unittest
from src.main.python.resources.utilities import utilities


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')
        cls.utils = utilities

    def setUp(self):
        print('Testing case:')


if __name__ == '__main__':
    unittest.main()
