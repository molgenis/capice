import unittest

import pandas as pd

from src.main.python.utilities.capice_imputing import CapiceImputing


class TestInputProcessor(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print('Setting up.')
        cls.imputing = CapiceImputing({})

    def test__calculate_percentage(self):
        actual = self.imputing._calculate_percentage(10, 100)
        self.assertEqual(10, actual)

    def test__correct_dtypes(self):
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'test': ['1', '2', '3'], 6: [1, 2, 3]})
        self.imputing.impute_values = {'test': 1, 6: 'test'}
        self.imputing._correct_dtypes(input_data_frame)
        self.assertEqual({'test': float, 6: str}, self.imputing.pre_dtypes)
        self.assertEqual({'test': int, 6: str}, self.imputing.dtypes)


if __name__ == '__main__':
    unittest.main()
