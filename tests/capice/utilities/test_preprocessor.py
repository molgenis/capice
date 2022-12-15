import unittest

import pandas as pd

from molgenis.capice.utilities.enums import Column
from molgenis.capice.utilities.categorical_processor import CategoricalProcessor


def get_uint8_array(values_list):
    return pd.array(values_list, dtype='uint8')


class TestPreprocessor(unittest.TestCase):
    @classmethod
    def setUp(cls):
        print('Setting up.')
        cls.preprocessor = CategoricalProcessor()
        cls.chr_pos_ref_alt_testcase = pd.DataFrame(
            {
                'chr': [1, 2, 3, 4, 5],
                'pos': [1, 2, 3, 4, 5],
                'REF': [1, 2, 3, 4, 5],
                'ALT': [1, 2, 3, 4, 5]
            }
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
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T']})
        expected_output = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T'],
             'chr_pos_ref_alt':
                 ['1_VeryUniqueCAPICESeparator_123_VeryUniqueCAPICESeparator_'
                  'A_VeryUniqueCAPICESeparator_G',
                  '2_VeryUniqueCAPICESeparator_456_VeryUniqueCAPICESeparator_'
                  'T_VeryUniqueCAPICESeparator_A',
                  '4_VeryUniqueCAPICESeparator_789_VeryUniqueCAPICESeparator_'
                  'C_VeryUniqueCAPICESeparator_T']
             }
        )
        actual_output = self.preprocessor._create_preservation_col(input_data_frame)

        pd.testing.assert_frame_equal(expected_output, actual_output)

    def test_is_train(self):
        self.assertEqual(False, self.preprocessor.train)

    def test__get_categorical_columns(self):
        preprocessor = CategoricalProcessor([], ['ref', 'alt'])
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T']})
        preprocessor._get_categorical_columns(input_data_frame)
        self.assertEqual(['ref', 'alt'], preprocessor.objects)

    def test__process_objects_train_false(self):
        self.preprocessor.objects = ['ref', 'alt', 'blaat']
        self.preprocessor.model_features = ['blaat_something']
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T'], 'blaat': ['some', 'value', 'something']})

        expected = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T'],
             'blaat_other': get_uint8_array([1, 1, 0]),
             'blaat_something': get_uint8_array([0, 0, 1])
             })
        observed = self.preprocessor._process_objects(input_data_frame)
        pd.testing.assert_frame_equal(expected, observed)

    def test__process_objects_train_true(self):
        self.preprocessor.train = True
        self.preprocessor.objects = ['ref', 'alt', 'blaat']
        self.preprocessor.model_features = ['blaat_something']
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T'], 'blaat': ['some', 'value', 'here']})
        expected = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref_A': get_uint8_array([1, 0, 0]),
             'ref_C': get_uint8_array([0, 0, 1]), 'ref_T': get_uint8_array([0, 1, 0]),
             'alt_A': get_uint8_array([0, 1, 0]), 'alt_G': get_uint8_array([1, 0, 0]),
             'alt_T': get_uint8_array([0, 0, 1]), 'blaat_here': get_uint8_array([0, 0, 1]),
             'blaat_some': get_uint8_array([1, 0, 0]),
             'blaat_value': get_uint8_array([0, 1, 0])})
        observed = self.preprocessor._process_objects(input_data_frame)
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
