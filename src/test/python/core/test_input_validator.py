import os
import unittest
import argparse
from pathlib import Path
from src.test.python.test_templates import teardown
from src.main.python.validators.validators import InputValidator
from src.main.python.utilities.utilities import get_project_root_dir
from src.main.python.utilities.input_processor import InputProcessor


class TestInputValidator(unittest.TestCase):
    temp_test_directory_name = '.another_test_output'
    temp_test_output = os.path.join(
        get_project_root_dir(),
        temp_test_directory_name
    )

    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.input_loc = os.path.join(get_project_root_dir(), 'CAPICE_example')
        root_dir = get_project_root_dir()
        cls.output_directory = os.path.join(root_dir, '.test_output')
        if not os.path.exists(cls.output_directory):
            os.makedirs(cls.output_directory)
        cls.call_dir = str(Path('.').absolute())
        cls.input_validator = InputValidator(argparse.ArgumentParser())
        cls.another_test_output = cls.temp_test_output
        cls.test_output_name = cls.temp_test_directory_name
        cls.input_file = os.path.join(
            '.',
            'CAPICE_example',
            'CAPICE_input.tsv.gz'
        )
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
        fake_input_file = os.path.join(self.input_loc, 'fakefile.tsv')
        self.assertRaises(
            SystemExit,
            self.input_validator.validate_input_loc,
            fake_input_file,
            'tsv'
        )

    def test_create_output_loc(self):
        print('Creating output location')
        with self.assertWarns(Warning):
            self.input_validator.validate_output_loc(self.another_test_output)
        self.assertTrue(
            self.test_output_name in os.listdir(get_project_root_dir())
        )

    def test_input_output_conversion_case1(self):
        """
        Test for the input validator if the correct input, output directory and
        output filename are set.
        Testing with only an input
        """
        print('Input output conversion (input only)')
        test_output = None
        input_processor = InputProcessor(
            input_path=self.input_file,
            output_path=test_output,
            force=False
        )
        expected_output_directory = self.call_dir
        self.assertEqual(
            input_processor.get_output_filename(),
            self.expected_output_filename
        )
        self.assertEqual(
            input_processor.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_case2(self):
        """
        Test for the input validator if the correct input, output directory and
        output filename are set.
        Testing with input and an output directory.
        """
        print('Input output conversion (input + output directory) (case2)')
        test_output = os.path.join('.', 'test_output')
        input_processor = InputProcessor(
            call_dir=self.call_dir,
            input_path=self.input_file,
            output_path=test_output,
            force=False
        )
        expected_output_directory = os.path.join('.', 'test_output')
        self.assertEqual(
            input_processor.get_output_filename(),
            self.expected_output_filename
        )
        self.assertEqual(
            input_processor.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_case3(self):
        """
        Test for the input validator if the correct input, output directory and
        output filename are set.
        Testing with input, output directory AND filename.
        """
        print('Input output conversion (input + output directory + filename)')
        test_output = os.path.join('.', 'test_output', self.test_filename)
        input_processor = InputProcessor(
            call_dir=self.call_dir,
            input_path=self.input_file,
            output_path=test_output,
            force=False
        )
        expected_output_directory = os.path.join('.', 'test_output')
        self.assertEqual(
            input_processor.get_output_filename(),
            self.test_filename
        )
        self.assertEqual(
            input_processor.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_case4(self):
        print('Input output conversion (input + filename)')
        input_processor = InputProcessor(
            call_dir=self.call_dir,
            input_path=self.input_file,
            output_path=self.test_filename,
            force=False
        )
        expected_output_directory = self.call_dir
        self.assertEqual(
            input_processor.get_output_filename(),
            self.test_filename
        )
        self.assertEqual(
            input_processor.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_train(self):
        print('Input output conversion for a train file')
        out_in_and_expected_out = 'foo.pickle.dat'
        input_processor = InputProcessor(
            call_dir=self.call_dir,
            input_path=self.input_file,
            output_path=out_in_and_expected_out,
            force=False
        )
        self.assertEqual(
            input_processor.get_output_filename(),
            out_in_and_expected_out
        )

    def test_input_output_conversion_output_already_present(self):
        print('Input output conversion with output already there')
        test_output = None
        with open(
                os.path.join(self.call_dir, self.expected_output_filename),
                'wt'
        ) as already_present_file:
            already_present_file.write('Some whitty comment')
        self.assertRaises(
            FileExistsError,
            InputProcessor,
            self.call_dir,
            self.input_file,
            test_output,
            False
        )
        os.remove(os.path.join(self.call_dir, self.expected_output_filename))

    def test_input_output_conversion_output_present_force_true(self):
        print('Input output conversion with output already present but '
              'force set to true')
        test_output = None
        input_processor = InputProcessor(
            call_dir=self.call_dir,
            input_path=self.input_file,
            output_path=test_output,
            force=True
        )
        expected_output_directory = self.call_dir
        with open(
                os.path.join(self.call_dir, self.expected_output_filename),
                'wt'
        ) as already_present_file:
            already_present_file.write('Some whitty comment')
        self.assertEqual(
            input_processor.get_output_filename(),
            self.expected_output_filename
        )
        self.assertEqual(
            input_processor.get_output_directory(),
            expected_output_directory
        )
        os.remove(os.path.join(self.call_dir, self.expected_output_filename))


if __name__ == '__main__':
    unittest.main()
