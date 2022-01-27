import os
import unittest
from pathlib import Path

from tests.capice.test_templates import _project_root_directory
from molgenis.capice.utilities.input_processor import InputProcessor


class TestInputProcessor(unittest.TestCase):

    __FILE__ = 'file_capice.txt'

    @classmethod
    def setUp(cls):
        print('Setting up.')
        output = os.path.join(
            _project_root_directory,
            'tests',
            'resources',
            'input_processor',
            'filename.txt'
        )
        cls.processor = InputProcessor('/test/input/file.txt', output, True, '.txt')

    def tearDown(self) -> None:
        potential_file = os.path.join(
            _project_root_directory,
            'tests',
            'resources',
            self.__FILE__
        )
        if os.path.isfile(potential_file):
            os.remove(potential_file)
        self.processor.force = True

    def test__set_output_path(self):
        output_dir = '/test/input/dir'
        filename = 'filename.txt'
        self.processor._set_output_path(output_dir, filename)
        self.assertEqual(self.processor.get_output_directory(), output_dir)
        self.assertEqual(self.processor.get_output_filename(), filename)

    def test_get_filename_from_path(self):
        path = '/test/input/dir/filename.txt'
        actual = self.processor.get_filename_from_path(path)
        self.assertEqual(actual, 'filename_capice.txt')

    def test__check_force(self):
        self.processor.force = False
        self.assertRaises(FileExistsError, self.processor._check_force)

    def test___handle_input_output_directories_case1(self):
        self.processor.output_path = None
        self.processor._handle_input_output_directories()
        self.assertEqual(str(Path('.').absolute()), self.processor.get_output_directory())
        self.assertEqual(self.__FILE__, self.processor.get_output_filename())

    def test___handle_input_output_directories_case2(self):
        self.processor.output_path = ''
        self.processor._handle_input_output_directories()
        self.assertEqual(str(Path('.').absolute()), self.processor.get_output_directory())
        self.assertEqual('', self.processor.get_output_filename())

    def test___handle_input_output_directories_case3(self):
        self.processor.output_path = '/something'
        self.processor._handle_input_output_directories()
        self.assertEqual('/something', self.processor.get_output_directory())
        self.assertEqual(self.__FILE__, self.processor.get_output_filename())

    def test___handle_input_output_directories_case4(self):
        self.processor.output_path = '/directory/file.txt'
        self.processor._handle_input_output_directories()
        self.assertEqual('/directory', self.processor.get_output_directory())
        self.assertEqual('file.txt', self.processor.get_output_filename())

    def test_force_false_output_missing_output_exists(self):
        # This test mimics what happens when output is left empty from the CLI
        # and the output file + _capice + default_extension already exists
        with open(
                os.path.join(
                    _project_root_directory,
                    'tests',
                    'resources',
                    self.__FILE__
                ), 'wt'
        ) as some_file:
            some_file.write('SomeString')
        self.processor.force = False
        self.assertRaises(
            FileExistsError,
            self.processor._handle_input_output_directories
        )


if __name__ == '__main__':
    unittest.main()
