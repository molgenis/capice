import unittest

import pandas as pd

from src.main.python.vep import seq


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.seq = seq.SEQ()

    def test_process(self):
        dataframe = pd.DataFrame(
            {'Seq': ['GATTTCCAGGNNNAACC', 'TTTTTGCCAACCC', 'TTTCCCGGANNNNNNNAAGGGTT', 'GTAACC']})
        observed = self.seq.process(dataframe)
        expected = pd.DataFrame({
            'Seq': ['GATTTCCAGGNNNAACC', 'TTTTTGCCAACCC', 'TTTCCCGGANNNNNNNAAGGGTT', 'GTAACC'],
            'GC': [0.48412, 0.46154, 0.47261, 0.50000],
            'CpG': [0.00375, 0.00000, 0.09727272727272727, 0.00000]})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
