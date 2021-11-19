import os
import unittest

from src.main.python.utilities.dynamic_loader import DynamicLoader
from src.main.python.utilities.utilities import get_project_root_dir
from src.test.python.test_templates import set_up_manager_and_loc


class TestDynamicLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up.')
        cls.manager, output = set_up_manager_and_loc()
        cls.correct_resources = os.path.join(
            get_project_root_dir(),
            'src',
            'test',
            'resources',
            'dynamic_loader_test_files_present'
        )
        cls.incorrect_resources = os.path.join(
            get_project_root_dir(),
            'src',
            'test',
            'resources',
            'dynamic_loader_test_no_files'
        )
        cls.required_attributes = ['name', 'some_function']

    @classmethod
    def tearDownClass(cls) -> None:
        print('Tearing down.')

    def setUp(self) -> None:
        print('Testing case:')

    def test_no_directory_given_raise(self):
        print('Raise OSError: no directory given')
        self.assertRaises(
            OSError,
            DynamicLoader,
            self.required_attributes,
            os.path.join(get_project_root_dir(), 'some_random_directory')
        )

    def test_manual_annotator_loader_correct(self):
        print('Loading correct manual annotator')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        loaded_modules = loader.load_manual_annotators()
        names = [module.name for module in loaded_modules]
        self.assertTrue('Correct' in names)

    def test_manual_annotator_loader_raise(self):
        print('Loading raise manual annotator no module found in correct directory')
        loader = DynamicLoader(
            required_attributes=['name', 'unrelated_function'],
            path=self.correct_resources
        )
        self.assertRaises(FileNotFoundError, loader.load_manual_annotators)

    def test_manual_annotator_loader_raise_no_module_found(self):
        print('Loading raise manual annotator no module found in wrong directory')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.incorrect_resources
        )
        self.assertRaises(FileNotFoundError, loader.load_manual_annotators)

    def test__check_dir_exists(self):
        print('')
        loader = DynamicLoader(required_attributes=[], path='/')
        loader.path = 'this/path/does/not/exist'
        self.assertRaises(OSError, loader._check_dir_exists)


if __name__ == '__main__':
    unittest.main()
