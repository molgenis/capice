import unittest

import pandas as pd

from molgenis.capice.vep import length


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.length = length.Length()

    def test_process(self):
        dataframe = pd.DataFrame({
            'REF': ['ATAG', 'A', 'C', 'AC'],
            'ALT': ['A', 'ATG', 'A', 'GT']})
        observed = self.length.process(dataframe)
        expected = pd.DataFrame({
            'REF': ['ATAG', 'A', 'C', 'AC'],
            'ALT': ['A', 'ATG', 'A', 'GT'],
            'Length': [3, 2, 0, 0]})
        expected = expected.astype({'Length': 'Int64'})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
