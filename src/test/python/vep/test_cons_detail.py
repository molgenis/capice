import unittest

import pandas as pd

from src.main.python.vep import cons_detail


class TestType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.cd = cons_detail.ConsDetail()

    def test_process(self):
        dataframe = pd.DataFrame({
            'Consequence': ['cq1_variant&cq2_region', 'cq3&cq4_gene', 'cq5_transcript']})
        observed = self.cd.process(dataframe)
        expected = pd.DataFrame(
            {'Consequence': ['cq1_variant&cq2_region', 'cq3&cq4_gene', 'cq5_transcript'],
             'ConsDetail': ['cq1,cq2', 'cq3,cq4', 'cq5']})
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
