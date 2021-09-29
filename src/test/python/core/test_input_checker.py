import os
import unittest
from pathlib import Path
from src.test.python.test_templates import teardown
from src.main.python.core.input_checker import InputChecker
from src.main.python.resources.errors.errors import InputError
from src.main.python.resources.utilities.utilities import get_project_root_dir


class TestInputChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.input_loc = os.path.join(get_project_root_dir(), 'CAPICE_example')
        root_dir = get_project_root_dir()
        cls.output_directory = os.path.join(root_dir, '.test_output')
        if not os.path.exists(cls.output_directory):
            os.makedirs(cls.output_directory)
        cls.input_checker = InputChecker()
        cls.call_dir = str(Path('.').absolute())

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        dir_to_be_deleted = os.path.join(
            get_project_root_dir(),
            '.another_test_output'
        )
        if os.path.isdir(dir_to_be_deleted):
            os.rmdir(dir_to_be_deleted)
        teardown()

    def setUp(self):
        print('Testing case:')

    def tearDown(self):
        print('Resetting arguments.')
        self.input_checker.output_filename = ''
        self.input_checker.output_directory = ''
        print('Arguments reset.')

    def test_input_error(self):
        print('Input file error')
        fake_input_file = os.path.join(self.input_loc, 'fakefile.tsv')
        with self.assertRaises(InputError) as context:
            self.input_checker.check_input_loc(fake_input_file)
        self.assertTrue(
            'Input file does not exist!'.startswith(str(context.exception))
        )

    def test_create_output_loc(self):
        print('Creating output location')
        dir_to_be_created = os.path.join(
            get_project_root_dir(),
            '.another_test_output'
        )
        self.input_checker.check_output_loc(dir_to_be_created)
        self.assertTrue(
            '.another_test_output' in os.listdir(get_project_root_dir())
        )

    def test_input_output_conversion_case1(self):
        """
        Test for the input checker if the correct input, output directory and
        output filename are set.
        Testing with only an input
        """
        print('Input output conversion (input only)')

        test_input = os.path.join('.', 'CAPICE_example', 'CAPICE_input.tsv.gz')
        test_output = None
        expected_output_filename = 'CAPICE_input_capice.tsv.gz'
        expected_output_directory = self.call_dir
        self.input_checker.check_input_output_directories(
            input_path=test_input,
            output_path=test_output
        )
        self.assertEqual(
            self.input_checker.get_output_filename(),
            expected_output_filename
        )
        self.assertEqual(
            self.input_checker.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_case2(self):
        """
        Test for the input checker if the correct input, output directory and
        output filename are set.
        Testing with input and an output directory.
        """
        print('Input output conversion (input + output directory)')

        test_input = os.path.join('.', 'CAPICE_example', 'CAPICE_input.tsv.gz')
        test_output = os.path.join('.', 'test_output')
        expected_output_filename = 'CAPICE_input_capice.tsv.gz'
        expected_output_directory = os.path.join('.', 'test_output')
        self.input_checker.check_input_output_directories(
            input_path=test_input,
            output_path=test_output
        )
        self.assertEqual(
            self.input_checker.get_output_filename(),
            expected_output_filename
        )
        self.assertEqual(
            self.input_checker.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_case3(self):
        """
        Test for the input checker if the correct input, output directory and
        output filename are set.
        Testing with input, output directory AND filename.
        """
        print('Input output conversion (input + output directory + filename)')
        test_input = os.path.join('.', 'CAPICE_example', 'CAPICE_input.tsv.gz')
        test_output = os.path.join('.', 'test_output', 'test.txt')
        expected_output_filename = 'test.txt.gz'
        expected_output_directory = os.path.join('.', 'test_output')
        self.input_checker.check_input_output_directories(
            input_path=test_input,
            output_path=test_output
        )
        self.assertEqual(
            self.input_checker.get_output_filename(),
            expected_output_filename
        )
        self.assertEqual(
            self.input_checker.get_output_directory(),
            expected_output_directory
        )

    def test_input_output_conversion_case4(self):
        print('Input output conversion (input + filename)')
        test_input = os.path.join('.', 'CAPICE_example', 'CAPICE_input.tsv.gz')
        test_output = 'test.txt'
        expected_output_filename = 'test.txt.gz'
        expected_output_directory = self.call_dir
        self.input_checker.check_input_output_directories(
            input_path=test_input,
            output_path=test_output
        )
        self.assertEqual(
            self.input_checker.get_output_filename(),
            expected_output_filename
        )
        self.assertEqual(
            self.input_checker.get_output_directory(),
            expected_output_directory
        )


if __name__ == '__main__':
    unittest.main()
