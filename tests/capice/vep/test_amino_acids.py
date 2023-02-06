import unittest

import pandas as pd

from molgenis.capice.vep import amino_acids


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
        expected = expected.astype({'oAA': 'category', 'nAA': 'category'})
        pd.testing.assert_frame_equal(expected, observed)

    def test_process_no_alt(self):
        dataframe = pd.DataFrame({'Amino_acids': ['A', 'R', 'G']})
        observed = self.aa.process(dataframe)
        expected = pd.DataFrame({'Amino_acids': ['A', 'R', 'G'],
                                 'oAA': ['A', 'R', 'G'],
                                 'nAA': ['A', 'R', 'G']})
        expected = expected.astype({'oAA': 'category', 'nAA': 'category'})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
