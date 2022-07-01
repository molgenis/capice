import unittest
import pandas as pd

from molgenis.capice.utilities import column_utils


class TestUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up')

    def setUp(self):
        print('\nTesting case:')
        self.column_utils = column_utils.ColumnUtils()
        self.column_utils.specified_columns = ['a', 'b', 'c']

    def test_set_specified_columns(self):
        """
        Test set_specified_columns
        Should set specified_columns of class
        """
        print('Setting specified columns')
        columns = ['x', 'y', 'z']
        self.column_utils.set_specified_columns(columns)
        self.assertEqual(columns, self.column_utils.get_specified_columns())

    def test_add_to_specified_columns(self):
        """
        Test add_to_specified_columns
        Should add string to specified_columns of class
        """
        print('Adding to specified columns')
        self.column_utils.add_to_specified_columns('d')
        self.assertEqual(['a', 'b', 'c', 'd'], self.column_utils.get_specified_columns())

    def test_column_in_specified_columns(self):
        """
        Test column_in_specified_columns
        Should return true because column is in specified_columns
        """
        print('Column is in specified columns')
        column = 'a'
        self.assertTrue(self.column_utils.column_in_specified_columns(column))

    def test_column_not_in_specified_columns(self):
        """
        Test column_in_specified_columns
        Should return false because column is not in specified_columns
        """
        print('Column not is in specified columns')
        column = 'x'
        self.assertFalse(self.column_utils.column_in_specified_columns(column))

    def test_get_missing_diff_with_list(self):
        """
        Test get_missing_diff_with with type list
        Should return "c" as missing column.
        """
        print('Get missings of diff with columns as list')
        columns = ['a', 'b', 'x', 'y']
        missing = self.column_utils.get_missing_diff_with(columns)
        self.assertEqual(['c'], missing)

    def test_get_missing_diff_with_dict_keys(self):
        """
        Test get_missing_diff_with with type dict keys
        Should return "c" as missing column.
        """
        print('Get missings of diff with columns of type dict keys')
        data = {'a': 0, 'b': 1, 'x': 3, 'y': 4}
        missing = self.column_utils.get_missing_diff_with(data.keys())
        self.assertEqual(['c'], missing)

    def test_get_missing_diff_with_pd_df(self):
        """
        Test get_missing_diff_with with type pandas dataframe
        Should return "cd" as missing column.
        """
        print('Get missings of diff with columns of type pandas dataframe')
        data = {'ab': 0, 'bc': 1, 'x': 3, 'y': 4}
        d = {'ab': [1, 2], 'bc': [3, 4], 'cd': [6, 8]}
        df = pd.DataFrame(data=d)
        self.column_utils.set_specified_columns(df.columns)
        missing = self.column_utils.get_missing_diff_with(data.keys())
        self.assertEqual(['cd'], missing)


if __name__ == '__main__':
    unittest.main()
