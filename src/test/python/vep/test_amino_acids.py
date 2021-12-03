import unittest

import pandas as pd

from src.main.python.vep import amino_acids


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.aa = amino_acids.AminoAcids()

    def test_process(self):
        dataframe = pd.DataFrame({'Amino_acids': ['A/G', 'R/C', 'G/C']})
        observed = self.aa.process(dataframe)
        expected = pd.DataFrame({'Amino_acids': ['A/G', 'R/C', 'G/C'],
                                 'oAA': ['A', 'R', 'G'],
                                 'nAA': ['G', 'C', 'C']})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
