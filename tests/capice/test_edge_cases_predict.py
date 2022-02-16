import os
import pickle
import unittest

import numpy as np
import pandas as pd

from tests.capice.test_templates import set_up_manager_and_out, teardown, set_up_predict, \
    _project_root_directory


class TestEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager, cls.output = set_up_manager_and_out()
        cls.edge_cases = os.path.join(
            _project_root_directory,
            'tests',
            'resources',
            'edge_cases_vep.tsv.gz'
        )
        cls.breakpoints = os.path.join(
            _project_root_directory,
            'tests',
            'resources',
            'breakends_vep.tsv.gz'
        )
        cls.symbolic = os.path.join(
            _project_root_directory,
            'tests',
            'resources',
            'symbolic_alleles_vep.tsv.gz'
        )
        with open(
                os.path.join(
                    _project_root_directory,
                    'tests',
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
            [0.42409733, 0.53885114, 0.45975062, 0.44440997, 0.56147087, 0.571394]
        ).astype(np.float64).rename('score')
        # rtol = atol = 0.0005, because 0.5 * 10 ** -3 = 0.0005 for a tolerance of 3 decimals
        pd.testing.assert_series_equal(
            observed_output['score'], expected_output, check_exact=False, rtol=0.0005, atol=0.0005
        )

    def test_symbolic_alleles(self):
        print('Symbolic alleles')
        self.main.infile = self.symbolic
        self.manager.output_filename = 'symbolic_alleles_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        expected_output = pd.Series(
            [0.42409733, 0.44440997, 0.55765855, 0.41767898, 0.4985433, 0.42409733]
        ).astype(np.float64).rename('score')
        # rtol = atol = 0.0005, because 0.5 * 10 ** -3 = 0.0005 for a tolerance of 3 decimals
        pd.testing.assert_series_equal(
            observed_output['score'], expected_output, check_exact=False, rtol=0.0005, atol=0.0005
        )

    def test_breakpoints(self):
        print('Breakpoints')
        self.main.infile = self.breakpoints
        self.manager.output_filename = 'breakends_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        expected_output = pd.Series(
            [0.517514, 0.42409733, 0.45975062, 0.571394, 0.4985433, 0.44440997]
        ).astype(np.float64).rename('score')
        # rtol = atol = 0.0005, because 0.5 * 10 ** -3 = 0.0005 for a tolerance of 3 decimals
        pd.testing.assert_series_equal(
            observed_output['score'], expected_output, check_exact=False, rtol=0.0005, atol=0.0005
        )


if __name__ == '__main__':
    unittest.main()
