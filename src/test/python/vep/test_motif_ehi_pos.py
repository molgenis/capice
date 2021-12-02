import unittest

import pandas as pd

from src.main.python.vep import motif_ehi_pos


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.score_change = motif_ehi_pos.MotifEHIPos()

    def test_process(self):
        dataframe = pd.DataFrame({'HIGH_INF_POS': ['Y', '1', 'M', '2']})
        observed = self.score_change.process(dataframe)
        expected = pd.DataFrame({'HIGH_INF_POS': ['Y', '1', 'M', '2'],
                                 'motifEHIPos': [1, 0, 0, 0]})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
