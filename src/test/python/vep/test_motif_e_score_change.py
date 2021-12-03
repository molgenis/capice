import unittest

import pandas as pd

from src.main.python.vep import motif_e_score_change


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.score_change = motif_e_score_change.MotifEScoreChange()

    def test_process(self):
        dataframe = pd.DataFrame({'MOTIF_SCORE_CHANGE': [1, 2, 3]})
        observed = self.score_change.process(dataframe)
        expected = pd.DataFrame({'MOTIF_SCORE_CHANGE': [1, 2, 3],
                                 'motifEScoreChng': [1, 2, 3]})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
