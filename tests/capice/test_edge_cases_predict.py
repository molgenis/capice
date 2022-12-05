import os
import unittest

import pandas as pd

from tests.capice.test_templates import set_up_manager_and_out, teardown, set_up_predict, \
    _project_root_directory, ResourceFile, load_model


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
        cls.model = load_model(ResourceFile.XGB_BOOSTER_POC_UBJ.value)
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
        self.assertGreater(observed_output['score'].sum(), 0)
        self.assertFalse(observed_output['score'].hasnans)

    def test_symbolic_alleles(self):
        print('Symbolic alleles')
        self.main.infile = self.symbolic
        self.manager.output_filename = 'symbolic_alleles_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        self.assertGreater(observed_output['score'].sum(), 0)
        self.assertFalse(observed_output['score'].hasnans)

    def test_breakpoints(self):
        print('Breakpoints')
        self.main.infile = self.breakpoints
        self.manager.output_filename = 'breakends_vep_capice.tsv.gz'
        self.main.run()
        observed_output = self.get_observed_results()
        self.assertGreater(observed_output['score'].sum(), 0)
        self.assertFalse(observed_output['score'].hasnans)


if __name__ == '__main__':
    unittest.main()
