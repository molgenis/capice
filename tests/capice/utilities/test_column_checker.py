import unittest

from molgenis.capice.utilities import column_checker


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')

    def setUp(self):
        print('\nTesting case:')
        self.cc = column_checker.ColumnChecker()
        self.cc.specified_columns = ['a', 'b', 'c']

    def test_set_specified_columns(self):
        print('Setting specified columns')
        columns = ['x', 'y', 'z']
        self.cc.set_specified_columns(columns)
        self.assertEqual(self.cc.get_specified_columns(), columns)

    def test_add_to_specified_columns(self):
        print('Adding to specified columns')
        self.cc.add_to_specified_columns('d')
        self.assertEqual(self.cc.get_specified_columns(), ['a', 'b', 'c', 'd'])

    def test_column_in_specified_columns(self):
        print('Column is in specified columns')
        column = 'a'
        self.assertTrue(self.cc.column_in_specified_columns(column))

    def test_column_not_in_specified_columns(self):
        print('Column not is in specified columns')
        column = 'x'
        self.assertFalse(self.cc.column_in_specified_columns(column))

    def test_get_missing_diff_with(self):
        print('Get missings of diff with columns')
        columns = ['a', 'b', 'x', 'y']
        missing = self.cc.get_missing_diff_with(columns)
        self.assertEqual(missing, ['c'])


if __name__ == '__main__':
    unittest.main()
