import os
import pickle
import unittest

import numpy as np
import pandas as pd

from src.main.python.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_out, teardown, set_up_predict


class TestEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager, cls.output = set_up_manager_and_out()
        cls.edge_cases = os.path.join(
            get_project_root_dir(),
            'src',
            'test',
            'resources',
            'edge_cases_vep.tsv.gz'
        )
        cls.breakpoints = os.path.join(
            get_project_root_dir(),
            'src',
            'test',
            'resources',
            'breakends_vep.tsv.gz'
        )
        cls.symbolic = os.path.join(
            get_project_root_dir(),
            'src',
            'test',
            'resources',
            'symbolic_alleles_vep.tsv.gz'
        )
        with open(
                os.path.join(
                    get_project_root_dir(),
                    'src',
                    'test',
                    'resources',
                    'xgb_booster_poc.pickle.dat'
                ), 'rb'
        ) as model_file:
            cls.model = pickle.load(model_file)
        cls.main = set_up_predict()

    @classmethod
    def tearDownClass(cls) -> None:
        teardown()

    def setUp(self) -> None:
        self.main = set_up_predict()
        self.main.output = self.output
        self.main.model = self.model
        print('Testing case:')

    def get_observed_results(self):
        return pd.read_csv(os.path.join(self.output, self.manager.output_filename), sep='\t')

    def test_edge_cases(self):
        print('Edge cases')
        self.main.infile = self.edge_cases
        self.manager.output_filename = 'edge_cases_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        expected_output = pd.Series(
            [0.34160867, 0.34160867, 0.4994438, 0.18767472, 0.18767472,
             0.18767472, 0.82134193,  0.82134193, 0.09479392, 0.09479392,
             0.82134193, 0.38768333, 0.5490537, 0.48907468]).astype(np.float64).rename('score')
        pd.testing.assert_series_equal(observed_output['score'], expected_output)

    def test_symbolic_alleles(self):
        print('Symbolic alleles')
        self.main.infile = self.symbolic
        self.manager.output_filename = 'symbolic_alleles_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        expected_output = pd.Series(
            [0.34160867, 0.4994438, 0.82134193, 0.82134193, 0.16419265, 0.16419265, 0.16419265,
             0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438,
             0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438,
             0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438,
             0.4994438, 0.4994438, 0.4994438, 0.4994438, 0.4994438]
        ).astype(np.float64).rename('score')
        pd.testing.assert_series_equal(observed_output['score'], expected_output)

    def test_breakpoints(self):
        print('Breakpoints')
        self.main.infile = self.breakpoints
        self.manager.output_filename = 'breakends_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        expected_output = pd.Series(
            [0.38156226, 0.34160867, 0.4994438, 0.4994438, 0.059770167, 0.059770167, 0.059770167,
             0.059770167, 0.100919195, 0.100919195, 0.100919195, 0.100919195]
        ).astype(np.float64).rename('score')
        pd.testing.assert_series_equal(observed_output['score'], expected_output)


if __name__ == '__main__':
    unittest.main()
