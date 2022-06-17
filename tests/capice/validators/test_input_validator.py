import os
import unittest

from molgenis.capice.validators.input_validator import InputValidator
from tests.capice.test_templates import _project_root_directory


class TestInputValidator(unittest.TestCase):
    new_directory_name = '.another_test_output_directory'
    new_directory = os.path.join(_project_root_directory, new_directory_name)

    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.input_validator = InputValidator()

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        if os.path.isdir(cls.new_directory):
            os.rmdir(cls.new_directory)

    def setUp(self):
        print('Testing case:')

    def test_input_error(self):
        print('Input file error')
        fake_input_file = os.path.join(_project_root_directory, 'fakefile.tsv')
        self.assertRaises(
            FileNotFoundError,
            self.input_validator.validate_input_path,
            fake_input_file,
            'tsv'
        )

    def test_input_extension_error(self):
        print('Input file extension error')
        fake_input_file = os.path.join(_project_root_directory, 'fakefile.csv')
        self.assertRaises(
            FileNotFoundError,
            self.input_validator.validate_input_path,
            fake_input_file,
            'tsv'
        )

    def test_create_output_path(self):
        print('Creating output location')
        with self.assertWarns(Warning):
            self.input_validator.validate_output_path(self.new_directory)
        self.assertTrue(
            self.new_directory_name in os.listdir(_project_root_directory)
        )

    def test_input_predict_correct(self):
        print('Input file predict correct')
        input_file = os.path.join(_project_root_directory, 'resources', 'predict_input.tsv.gz')
        self.input_validator.validate_input_path(input_file, extension=('.tsv', '.tsv.gz'))

    def test_input_explain_correct(self):
        print('Input file explain correct')
        input_file = os.path.join(_project_root_directory, 'tests', 'resources',
                                  'xgb_booster_poc.pickle.dat')
        self.input_validator.validate_input_path(input_file, extension='.pickle.dat')


if __name__ == '__main__':
    unittest.main()
