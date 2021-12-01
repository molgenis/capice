import unittest

import pandas as pd

from src.main.python.utilities.preprocessor import PreProcessor


def get_uint8_array(values_list):
    return pd.array(values_list, dtype='uint8')


class TestPreprocessor(unittest.TestCase):
    @classmethod
    def setUp(cls):
        print('Setting up.')
        cls.preprocessor = PreProcessor([])

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

    def test__is_train(self):
        self.assertEqual(False, self.preprocessor.train)
        self.preprocessor._is_train()
        self.assertEqual(True, self.preprocessor.train)

    def test__get_categorical_columns(self):
        input_data_frame = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref': ['A', 'T', 'C'],
             'alt': ['G', 'A', 'T']})
        self.preprocessor._get_categorical_columns(input_data_frame)
        self.assertEqual(['ref', 'alt'], self.preprocessor.objects)

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
             'alt': ['G', 'A', 'T'], 'blaat': ['some', 'value', 'here'], 'Domain': ['1', '2', '3']})
        expected = pd.DataFrame(
            {'chr': [1, 2, 4], 'pos': [123, 456, 789], 'ref_A': get_uint8_array([1, 0, 0]),
             'ref_C': get_uint8_array([0, 0, 1]), 'ref_T': get_uint8_array([0, 1, 0]),
             'alt_A': get_uint8_array([0, 1, 0]), 'alt_G': get_uint8_array([1, 0, 0]),
             'alt_T': get_uint8_array([0, 0, 1]), 'Domain_1': get_uint8_array([1, 0, 0]),
             'Domain_2': get_uint8_array([0, 1, 0]), 'Domain_3': get_uint8_array([0, 0, 1]),
             'blaat_here': get_uint8_array([0, 0, 1]), 'blaat_some': get_uint8_array([1, 0, 0]),
             'blaat_value': get_uint8_array([0, 1, 0])})
        observed = self.preprocessor._process_objects(input_data_frame)
        pd.testing.assert_frame_equal(expected, observed)


if __name__ == '__main__':
    unittest.main()
