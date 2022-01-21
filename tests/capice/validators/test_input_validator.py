import argparse
import os
import unittest
from pathlib import Path

from molgenis.capice.validators.input_validator import InputValidator
from tests.capice.test_templates import teardown, _project_root_directory


class TestInputValidator(unittest.TestCase):
    temp_test_directory_name = '.another_test_output'
    temp_test_output = os.path.join(
        _project_root_directory,
        temp_test_directory_name
    )

    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.input_path = os.path.join(_project_root_directory, 'CAPICE_example')
        root_dir = _project_root_directory
        cls.output_directory = os.path.join(root_dir, '.test_output')
        if not os.path.exists(cls.output_directory):
            os.makedirs(cls.output_directory)
        cls.call_dir = str(Path('.').absolute())
        cls.input_validator = InputValidator(argparse.ArgumentParser())
        cls.another_test_output = cls.temp_test_output
        cls.test_output_name = cls.temp_test_directory_name
        cls.input_file = os.path.join(cls.input_path, 'CAPICE_input.tsv.gz')
        cls.expected_output_filename = 'CAPICE_input_capice'
        cls.test_filename = 'test.txt'

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        if os.path.isdir(cls.temp_test_output):
            os.rmdir(cls.temp_test_output)
        teardown()

    def setUp(self):
        print('Testing case:')

    def tearDown(self):
        print('Resetting arguments.')
        self.input_validator.output_filename = ''
        self.input_validator.output_directory = ''
        print('Arguments reset.')

    def test_input_error(self):
        print('Input file error')
        fake_input_file = os.path.join(self.input_path, 'fakefile.tsv')
        self.assertRaises(
            SystemExit,
            self.input_validator.validate_input_path,
            fake_input_file,
            'tsv'
        )

    def test_create_output_path(self):
        print('Creating output location')
        with self.assertWarns(Warning):
            self.input_validator.validate_output_path(self.another_test_output)
        self.assertTrue(
            self.test_output_name in os.listdir(_project_root_directory)
        )


if __name__ == '__main__':
    unittest.main()
