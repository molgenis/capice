import unittest

import numpy as np
import pandas as pd

from molgenis.capice.vep.sift import SIFT


class TestSift(unittest.TestCase):
    def test_sift(self):
        dataset = pd.DataFrame(
            {
                'SIFT': [np.nan, 0.002, 0.05, 0.9]
            }
        )
        expected = pd.concat(
            [
                dataset,
                pd.DataFrame(
                    {
                        'SIFTval': [np.nan, 0.002, 0.05, 0.9],
                        'SIFTcat': [np.nan, 'deleterious', 'deleterious', 'tolerated']
                    }
                )
            ], axis=1
        )
        observed = SIFT().process(dataset)
        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(axis=1))

    def test_sift_full_nan(self):
        list_of_nans = [np.nan, np.nan, np.nan]
        dataset = pd.DataFrame(
            {
                'SIFT': list_of_nans
            }
        )
        expected = pd.concat(
            [
                dataset,
                pd.DataFrame(
                    {
                        'SIFTval': list_of_nans,
                        'SIFTcat': list_of_nans
                    }
                )
            ], axis=1
        )
        observed = SIFT().process(dataset)
        pd.testing.assert_frame_equal(observed.sort_index(axis=1), expected.sort_index(axis=1))


if __name__ == '__main__':
    unittest.main()
