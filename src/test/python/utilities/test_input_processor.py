import os
import unittest

from src.main.python.utilities.input_processor import InputProcessor
from src.main.python.utilities.utilities import get_project_root_dir


class TestInputProcessor(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print('Setting up.')
        output = str(get_project_root_dir()) + \
                 '/src/test/resources/input_processor/filename.txt'
        cls.processor = InputProcessor('/test/input/dir', output, True)

    def test__set_output_path(self):
        output_dir = '/test/input/dir'
        filename = 'filename.txt'
        self.processor._set_output_path(output_dir, filename)
        self.assertEqual(self.processor.get_output_directory(), output_dir)
        self.assertEqual(self.processor.get_output_filename(), filename)

    def test_get_filename_from_path(self):
        path = '/test/input/dir/filename.txt'
        actual = self.processor.get_filename_from_path(path)
        self.assertEqual(actual, 'filename_capice')

    def test__check_force(self):
        self.processor.force = False
        self.assertRaises(FileExistsError, self.processor._check_force)
