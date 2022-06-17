import unittest
import pandas as pd

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
        self.assertEqual(columns, self.cc.get_specified_columns())

    def test_add_to_specified_columns(self):
        print('Adding to specified columns')
        self.cc.add_to_specified_columns('d')
        self.assertEqual(['a', 'b', 'c', 'd'], self.cc.get_specified_columns())

    def test_column_in_specified_columns(self):
        print('Column is in specified columns')
        column = 'a'
        self.assertTrue(self.cc.column_in_specified_columns(column))

    def test_column_not_in_specified_columns(self):
        print('Column not is in specified columns')
        column = 'x'
        self.assertFalse(self.cc.column_in_specified_columns(column))

    def test_get_missing_diff_with_list(self):
        print('Get missings of diff with columns as list')
        columns = ['a', 'b', 'x', 'y']
        missing = self.cc.get_missing_diff_with(columns)
        self.assertEqual(['c'], missing)

    def test_get_missing_diff_with_dict_keys(self):
        print('Get missings of diff with columns of type dict keys')
        data = {'a': 0, 'b': 1, 'x': 3, 'y': 4}
        missing = self.cc.get_missing_diff_with(data.keys())
        self.assertEqual(['c'], missing)

    def test_get_missing_diff_with_pd_df(self):
        print('Get missings of diff with columns of type dict keys')
        data = {'ab': 0, 'bc': 1, 'x': 3, 'y': 4}
        d = {'ab': [1, 2], 'bc': [3, 4], 'cd': [6, 8]}
        df = pd.DataFrame(data=d)
        self.cc.set_specified_columns(df.columns)
        missing = self.cc.get_missing_diff_with(data.keys())
        self.assertEqual(['cd'], missing)


if __name__ == '__main__':
    unittest.main()
