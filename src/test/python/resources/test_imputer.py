import os
import pickle
import unittest
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc, teardown, \
    set_up_main


class TestImputer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager, output_loc = set_up_manager_and_loc()
        cls.vep_version = 104.0
        cls.grch_build = 37
        cls.impute_overwrite = 'VEP104'
        cls.main = set_up_main()
        cls.main.infile = os.path.join(
            get_project_root_dir(),
            'CAPICE_example',
            'CAPICE_input.tsv.gz'
        )
        with open(
                os.path.join(
                    get_project_root_dir(),
                    'CAPICE_model',
                    'GRCh37',
                    'POC',
                    'xgb_booster_poc.pickle.dat'
                ), 'rb'
        ) as model_file:
            cls.model = pickle.load(model_file)
        cls.main.model = cls.model

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_unit_imputation_file(self):
        """
        Unit test for imputation to be called with only the file header
        information.
        """
        print('Imputing (unit) (file)')
        self.main.impute(
            loaded_data=self.main.process(
                self.main.load_file()
            )
        )

    def test_component_imputation(self):
        """
        component test for the imputer to see if there are any gaps after the
        imputer has processed the data.
        """
        print('Imputing (component)')
        imputed_file = self.main.impute(
            loaded_data=self.main.process(
                self.main.load_file()
            )
        )
        self.assertFalse(
            imputed_file[self.model.impute_values.keys()].isnull().values.any()
        )


if __name__ == '__main__':
    unittest.main()
