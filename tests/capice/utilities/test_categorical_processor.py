import unittest

import numpy as np
import pandas as pd

from molgenis.capice.utilities.enums import Column
from tests.capice.test_templates import set_up_impute_preprocess, teardown
from molgenis.capice.utilities.categorical_processor import CategoricalProcessor


class TestCategoricalProcessor(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.preprocessor = CategoricalProcessor()
        cls.chr_pos_ref_alt_testcase = pd.DataFrame(
            {
                'chr': [1, 2, 3, 4, 5],
                'pos': [1, 2, 3, 4, 5],
                'REF': [1, 2, 3, 4, 5],
                'ALT': [1, 2, 3, 4, 5]
            }
        )
        cls.main, cls.model = set_up_impute_preprocess()

    @classmethod
    def tearDownClass(cls) -> None:
        teardown()

    def test_unit_preprocessing_file(self):
        """
        Unit test for the preprocessor to see if the preprocessor works just
        the file header information.
        """
        print('Preprocessing (unit) (file)')
        self.main.categorical_process(
            loaded_data=self.main.process(
                self.main._load_file()
            ), processing_features=self.model.processable_features
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
        processed_file = self.main.categorical_process(
            loaded_data=self.main.process(
                self.main._load_file()
            ), processing_features=self.model.processable_features
        )[0]
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
                'REF': ['A', 'T', 'A', 'T', 'A', 'T'],
                'ALT': ['G', 'C', 'G', 'C', 'G', 'C']
            }
        )
        user_input_features = ['foo', 'bar', 'baz', 'feature_1']
        processor = CategoricalProcessor()
        observed = processor.process(data, processable_features=user_input_features)[0]
        expected = pd.DataFrame(
            {
                'foo_a': [1, 0, 0, 0, 0, 0],
                'foo_b': [0, 1, 0, 0, 0, 0],
                'foo_c': [0, 0, 1, 0, 0, 0],
                'foo_other_CAPICE_value': [0, 0, 0, 1, 1, 1],
                'bar_a': [1, 0, 0, 0, 0, 0],
                'bar_other_CAPICE_value': [0, 1, 1, 1, 1, 1],
                'baz_a': [1, 0, 0, 0, 0, 0],
                'baz_b': [0, 1, 0, 0, 0, 0],
                'baz_c': [0, 0, 1, 0, 0, 0],
                'baz_d': [0, 0, 0, 1, 0, 0],
                'baz_e': [0, 0, 0, 0, 1, 0],
                'baz_other_CAPICE_value': [0, 0, 0, 0, 0, 1],
                'REF': ['A', 'T', 'A', 'T', 'A', 'T'],
                'ALT': ['G', 'C', 'G', 'C', 'G', 'C'],
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

    def test_creation_other(self):
        test_case = pd.concat(
            [
                self.chr_pos_ref_alt_testcase,
                pd.DataFrame(
                    {
                        'foo': ['bar', 'baz', 'barz', 'foobar', 'foobaz', 'last']
                    }
                )
            ], axis=1
        )
        observed_df, observed_dict = self.preprocessor.process(test_case, processable_features=[
            'foo'])
        self.assertIn(
            'foo',
            observed_dict.keys()
        )
        self.assertIn(
            Column.other.value,
            observed_dict['foo']
        )
        self.assertIn('foo_other_CAPICE_value', observed_df.columns)

    def test_creation_other_notin(self):
        test_case = pd.concat(
            [
                self.chr_pos_ref_alt_testcase,
                pd.DataFrame(
                    {
                        'foo': ['bar', 'baz', 'barz', 'foobar', 'foobaz']
                    }
                )
            ], axis=1
        )
        observed_df, observed_dict = self.preprocessor.process(test_case, processable_features=[
            'foo'])
        self.assertIn(
            'foo',
            observed_dict.keys()
        )
        self.assertNotIn(
            'other',
            observed_dict['foo']
        )
        self.assertNotIn('foo_other', observed_df.columns)

    def test_other_in_top_5(self):
        # Tests that, if "other" occurs in the top 5 categories, only this "other" feature gets
        # sampled and no other sample get sampled into the "other" category.
        test_case = pd.concat(
            [
                self.chr_pos_ref_alt_testcase,
                pd.DataFrame(
                    {
                        'foo': ['other', 'other', 'foo', 'bar', 'baz', 'foobar', 'foobaz']
                    }
                )
            ], axis=1
        )
        observed_df, observed_dict = self.preprocessor.process(test_case, processable_features=[
            'foo'])
        test_series = observed_df['foo_other']
        self.assertFalse(test_series[test_series > 0].size > 2,
                         msg=f'Actual size: {test_series[test_series > 0].size}')
        self.assertIn(
            'foo_other_CAPICE_value',
            observed_df.columns
        )

    def test__create_preservation_col(self):
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'REF': ['A', 'T', 'C'],
             'ALT': ['G', 'A', 'T']})
        expected_output = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'REF': ['A', 'T', 'C'],
             'ALT': ['G', 'A', 'T'],
             'chr_pos_ref_alt':
                 ['1_VeryUniqueCAPICESeparator_123_VeryUniqueCAPICESeparator_'
                  'A_VeryUniqueCAPICESeparator_G',
                  '2_VeryUniqueCAPICESeparator_456_VeryUniqueCAPICESeparator_'
                  'T_VeryUniqueCAPICESeparator_A',
                  '4_VeryUniqueCAPICESeparator_789_VeryUniqueCAPICESeparator_'
                  'C_VeryUniqueCAPICESeparator_T']
             }
        )
        self.preprocessor._create_preservation_col(input_data_frame)

        pd.testing.assert_frame_equal(expected_output, input_data_frame)

    def test__get_categorical_columns(self):
        preprocessor = CategoricalProcessor()
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'REF': ['A', 'T', 'C'],
             'ALT': ['G', 'A', 'T']})
        features = preprocessor._get_categorical_columns(input_data_frame, processable_features=[
            'REF', 'ALT'])
        self.assertIn('REF', features.keys())
        self.assertIn('ALT', features.keys())


if __name__ == '__main__':
    unittest.main()
