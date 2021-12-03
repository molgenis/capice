import unittest

import numpy as np
import pandas as pd

from src.main.python.vep import cdna_position


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.cdna_pos = cdna_position.CDNAPosition()

    def test_process(self):
        dataframe = pd.DataFrame({'cDNA_position': ['305/702', '60/550', '?-/123', '-?/456']})
        observed = self.cdna_pos.process(dataframe)
        expected = pd.DataFrame({'cDNA_position': ['305/702', '60/550', '?-/123', '-?/456'],
                                 'cDNApos': [305.00000, 60.00000, np.nan, np.nan],
                                 'relcDNApos': [702.00000, 550.0000, 123.00000, 456.00000]})
        pd.testing.assert_frame_equal(expected, observed)

    def test_corner_case(self):
        dataframe = pd.DataFrame(
            {
                'cDNA_position': ['483-486', '162-163']
            }
        )
        observed = self.cdna_pos.process(dataframe)
        expected = pd.DataFrame({'cDNA_position': ['483-486', '162-163'],
                                 'cDNApos': [483.00000, 162.00000],
                                 'relcDNApos': [np.nan, np.nan]})
        pd.testing.assert_frame_equal(expected, observed)

    def test_process_nan(self):
        dataframe = pd.DataFrame({'cDNA_position': [np.nan, np.nan]})
        observed = self.cdna_pos.process(dataframe)
        expected = pd.DataFrame({'cDNA_position': [np.nan, np.nan],
                                 'cDNApos': [np.nan, np.nan],
                                 'relcDNApos': [np.nan, np.nan]})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
