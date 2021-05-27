import unittest
from src.main.python.resources.utilities import utilities


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')
        cls.utils = utilities

    def setUp(self):
        print('Testing case:')

    def test_cla_string_conversion_list(self):
        print('CLA (list) to string.')
        cla = ['This is a test']
        converted = self.utils.convert_cla_to_str(cla)
        self.assertIn(converted, cla)

    def test_cla_string_conversion_nolist(self):
        print('CLA (no list) to string.')
        cla = 'This is a test'
        converted = self.utils.convert_cla_to_str(cla)
        self.assertEqual(cla, converted)


if __name__ == '__main__':
    unittest.main()
