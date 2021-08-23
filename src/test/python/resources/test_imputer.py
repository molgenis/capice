import os
import unittest
import pandas as pd
from src.main.python.resources.imputers.capice_imputing import CapiceImputing
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

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def tearDown(self):
        print('Resetting arguments.')
        self.manager.overwrite_impute = False
        self.manager.vep_version = False
        self.manager.grch_build = False
        print('Arguments reset.')

    def test_unit_imputation_config(self):
        """
        Unit test for imputation to be called with config specific arguments.
        """
        print('Imputing (unit) (config)')
        self.manager.vep_version = self.vep_version
        self.manager.grch_build = self.grch_build
        self.main.impute(
            loaded_data=self.main.annotate(
                self.main.load_file()
            )
        )

    def test_unit_imputation_file(self):
        """
        Unit test for imputation to be called with only the file header
        information.
        """
        print('Imputing (unit) (file)')
        self.main.impute(
            loaded_data=self.main.annotate(
                self.main.load_file()
            )
        )

    def test_unit_imputation_overwrite(self):
        """
        Unit test for imputation to be called with only the overwrite config
        variable.
        """
        print('Imputing (unit) (overwrite)')
        self.manager.overwrite_impute = self.impute_overwrite
        self.main.impute(
            loaded_data=self.main.annotate(
                self.main.load_file()
            )
        )

    def test_component_imputation(self):
        """
        component test for the imputer to see if there are any gaps after the
        imputer has processed the data.
        """
        print('Imputing (component)')
        self.manager.overwrite_impute = self.impute_overwrite
        imputed_file = self.main.impute(
            loaded_data=self.main.annotate(
                self.main.load_file()
            )
        )
        imputed_columns = self.manager.annotation_features
        print(imputed_columns)
        self.assertFalse(imputed_file[imputed_columns].isnull().values.any())

    def test_empty_chrom(self):
        print('Empty Chr entry in input data')
        dataset = pd.DataFrame(
            {
                'Chr': [1, 2, None, 3],
                'Pos': [100, None, 300, 400]
            }
        )
        remainin_dataset = pd.DataFrame(
            {
                'Chr': ["1", "3"],
                'Pos': [100, 400]
            }
        )
        self.manager.overwrite_impute = self.impute_overwrite
        imputer = CapiceImputing(train=False)
        processed_dataframe = imputer._check_chrom_pos(dataset=dataset)
        pd.testing.assert_frame_equal(processed_dataframe, remainin_dataset)


if __name__ == '__main__':
    unittest.main()
