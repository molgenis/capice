import unittest

import numpy as np
import pandas as pd

from tests.capice.test_templates import set_up_impute_preprocess, teardown
from molgenis.capice.utilities.categorical_processor import CategoricalProcessor


class TestPreprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.main, cls.model = set_up_impute_preprocess()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_unit_preprocessing_file(self):
        """
        Unit test for the preprocessor to see if the preprocessor works just
        the file header information.
        """
        print('Preprocessing (unit) (file)')
        self.main.process(
            loaded_data=self.main.process(
                    self.main._load_file(), process_features=self.model.vep_features
                ), input_features=self.model.get_booster().feature_names
        )

    def test_component_preprocessing(self):
        """
        component test for preprocessing. All columns within the CADD
        features should be processed. Furthermore,
        within all processed columns,
        there should not be 1 or more column that is still
        considered categorical.
        """
        print('Preprocessing (component)')
        processed_file = self.main.process(
            self.main.process(
                self.main._load_file(), process_features=self.model.vep_features
            ), input_features=self.model.get_booster().feature_names
        )
        model_features = self.model.get_booster().feature_names
        processed_columns = processed_file.columns
        for feature in model_features:
            # Check if all model features are present before predicting
            self.assertIn(feature, processed_columns)
        # Check if none of the processed columns can be marked as categorical
        self.assertEqual(
            len(processed_file[model_features].select_dtypes(include=["O"]).columns),
            0
        )

    def test_preprocessing_train(self):
        """
        Component test for the preprocessing part with train=True.
        """
        data = pd.DataFrame(
            {
                'foo': ['a', 'b', 'c', np.nan, np.nan, np.nan],
                'bar': ['a', np.nan, np.nan, np.nan, np.nan, np.nan],
                'baz': ['a', 'b', 'c', 'd', 'e', 'f'],
                'feature_1': [1, 2, 3, 4, np.nan, np.nan],
                'feature_excluded': [1, 2, 3, 4, np.nan, np.nan],
                'chr': [1, 2, 3, 4, 5, 6],
                'pos': [100, 200, 300, 400, 500, 600],
                'ref': ['A', 'T', 'A', 'T', 'A', 'T'],
                'alt': ['G', 'C', 'G', 'C', 'G', 'C']
            }
        )
        user_input_features = ['foo', 'bar', 'baz', 'feature_1']
        processor = CategoricalProcessor(
            exclude_features=['feature_excluded'], input_features=user_input_features, train=True
        )
        observed = processor.process(data)
        expected = pd.DataFrame(
            {
                'foo_a': [1, 0, 0, 0, 0, 0],
                'foo_b': [0, 1, 0, 0, 0, 0],
                'foo_c': [0, 0, 1, 0, 0, 0],
                'foo_other': [0, 0, 0, 1, 1, 1],
                'bar_a': [1, 0, 0, 0, 0, 0],
                'bar_other': [0, 1, 1, 1, 1, 1],
                'baz_a': [1, 0, 0, 0, 0, 0],
                'baz_b': [0, 1, 0, 0, 0, 0],
                'baz_c': [0, 0, 1, 0, 0, 0],
                'baz_d': [0, 0, 0, 1, 0, 0],
                'baz_e': [0, 0, 0, 0, 1, 0],
                'baz_other': [0, 0, 0, 0, 0, 1],
                'ref_A': [1, 0, 1, 0, 1, 0],
                'ref_T': [0, 1, 0, 1, 0, 1],
                'alt_G': [1, 0, 1, 0, 1, 0],
                'alt_C': [0, 1, 0, 1, 0, 1],
                'feature_1': [1, 2, 3, 4, np.nan, np.nan],
                'feature_excluded': [1, 2, 3, 4, np.nan, np.nan],
                'chr': [1, 2, 3, 4, 5, 6],
                'pos': [100, 200, 300, 400, 500, 600],
                'chr_pos_ref_alt': [
                    '1_VeryUniqueCAPICESeparator_100_VeryUniqueCAPICESeparator_'
                    'A_VeryUniqueCAPICESeparator_G',
                    '2_VeryUniqueCAPICESeparator_200_VeryUniqueCAPICESeparator_'
                    'T_VeryUniqueCAPICESeparator_C',
                    '3_VeryUniqueCAPICESeparator_300_VeryUniqueCAPICESeparator_'
                    'A_VeryUniqueCAPICESeparator_G',
                    '4_VeryUniqueCAPICESeparator_400_VeryUniqueCAPICESeparator_'
                    'T_VeryUniqueCAPICESeparator_C',
                    '5_VeryUniqueCAPICESeparator_500_VeryUniqueCAPICESeparator_'
                    'A_VeryUniqueCAPICESeparator_G',
                    '6_VeryUniqueCAPICESeparator_600_VeryUniqueCAPICESeparator_'
                    'T_VeryUniqueCAPICESeparator_C',
                ]
            }
        )
        pd.testing.assert_frame_equal(
            observed.sort_index(axis=1), expected.sort_index(axis=1), check_dtype=False
        )


if __name__ == '__main__':
    unittest.main()
