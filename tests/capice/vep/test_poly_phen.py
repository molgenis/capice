import unittest

import numpy as np
import pandas as pd

from molgenis.capice.vep import poly_phen


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.poly_phen = poly_phen.PolyPhen()

    def test_process(self):
        dataframe = pd.DataFrame(
            {
                'PolyPhen': [0.445, 0.908, 0.999, np.nan]
            }
        )
        expected = pd.concat(
            [
                dataframe,
                pd.DataFrame(
                    {
                        'PolyPhenCat': ['benign', 'possibly_damaging', 'probably_damaging', np.nan],
                        'PolyPhenVal': [0.445, 0.908, 0.999, np.nan]
                    }
                )
            ], axis=1
        )
        observed = self.poly_phen.process(dataframe)
        pd.testing.assert_frame_equal(expected.sort_index(axis=1), observed.sort_index(axis=1))


if __name__ == '__main__':
    unittest.main()
