import unittest

import numpy as np
import pandas as pd

from src.main.python.vep import poly_phen


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.poly_phen = poly_phen.PolyPhen()

    def test_process(self):
        dataframe = pd.DataFrame(
            {'PolyPhen': ['benign(0.08)', 'possibly_damaging(0.822)', np.nan]})
        observed = self.poly_phen.process(dataframe)
        expected = pd.DataFrame({'PolyPhen': ['benign(0.08)', 'possibly_damaging(0.822)', np.nan],
                                 'PolyPhenCat': ['benign', 'possibly_damaging', np.nan],
                                 'PolyPhenVal': [0.08, 0.822, np.nan]})
        pd.testing.assert_frame_equal(expected, observed)

    def test_process_nan(self):
        dataframe = pd.DataFrame(
            {'PolyPhen': [np.nan]})
        observed = self.poly_phen.process(dataframe)
        expected = pd.DataFrame({'PolyPhen': [np.nan],
                                 'PolyPhenCat': [np.nan],
                                 'PolyPhenVal': [np.nan]})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
