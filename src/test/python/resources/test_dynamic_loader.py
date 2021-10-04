import io
import os
import sys
import unittest
from src.test.python.test_templates import set_up_manager_and_loc
from src.main.python.resources.utilities.dynamic_loader import DynamicLoader
from src.main.python.resources.utilities.utilities import get_project_root_dir
from src.main.python.core.logger import Logger


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
        cls.correct_vep = 104.0
        cls.correct_grch = 37

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
        names = []
        for module in loaded_modules:
            names.append(module.name)
        self.assertTrue('Correct' in names)

    def test_manual_annotator_loader_raise(self):
        print('Loading raise manual annotator no module found in '
              'correct directory')
        loader = DynamicLoader(
            required_attributes=['name', 'unrelated_function'],
            path=self.correct_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_manual_annotators
        )

    def test_manual_annotator_loader_raise_no_module_found(self):
        print('Loading raise manual annotator no module found in '
              'wrong directory')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.incorrect_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_manual_annotators
        )

    def test_impute_preprocessor_loader_correct_vep_grch(self):
        print('impute_preprocessor_loader with correct VEP and GRCh arguments')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        module = loader.load_impute_preprocess_modules(
            vep_version=self.correct_vep,
            grch_build=self.correct_grch,
            overwrite=None
        )
        self.assertEqual('SomeVeryUniqueString', module.some_function())

    def test_impute_preprocessor_loader_correct_overwrite(self):
        print('impute_preprocessor_loader with correct overwrite')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        module = loader.load_impute_preprocess_modules(
            vep_version=None,
            grch_build=None,
            overwrite='Correct_Overwrite'
        )
        self.assertEqual(
            'SomeVeryUniqueString_butdifferent', module.some_function()
        )

    def test_impute_preprocessor_loader_raise_vep(self):
        print('impute_preprocessor_loader with raise due to VEP mismatch')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_impute_preprocess_modules,
            0,
            self.correct_grch,
            None
        )

    def test_impute_preprocessor_loader_raise_grch(self):
        print('impute_preprocessor_loader with raise due to GRCh mismatch')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_impute_preprocess_modules,
            self.correct_vep,
            0,
            None
        )

    def test_impute_preprocessor_loader_raise_different_files(self):
        print('impute_preprocessor_loader with raise due to VEP and GRCh '
              'both correct but in different files')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_impute_preprocess_modules,
            None,
            self.correct_grch,
            None
        )

    def test_impute_preprocessor_loader_raise_both(self):
        print('impute_preprocessor_loader with raise due to both VEP and GRCh '
              'mismatch')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_impute_preprocess_modules,
            0,
            0,
            None
        )

    def test_impute_preprocessor_loader_raise_overwrite(self):
        print('impute_preprocessor_loader with raise due to overwrite mismatch')
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        self.assertRaises(
            FileNotFoundError,
            loader.load_impute_preprocess_modules,
            0,
            0,
            'Unrelated'
        )

    def test_impute_preprocessor_loader_vep_grch_dupe(self):
        print(
            'Duplicates when using VEP version and GRCh build in '
            'impute_preprocessor_loader'
        )
        # Reset logger instance
        Logger.instance = None
        self.manager.critical_logging_only = False

        # Capture stderr
        old_stderr = sys.stderr
        listener = io.StringIO()
        sys.stderr = listener

        # Do the usual stuff
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        loader.load_impute_preprocess_modules(
            vep_version=self.correct_vep,
            grch_build=self.correct_grch,
            overwrite=None
        )

        # Get stderr
        out = listener.getvalue()
        sys.stderr = old_stderr

        # Test
        self.assertTrue(
            f"WARNING: Found multiple matches for VEP version "
            f"{self.correct_vep} and GRCh build {self.correct_grch}!" in out)

        # Reset logger to it's original state
        Logger.instance = None
        self.manager.critical_logging_only = True

    def test_impute_preprocessor_loader_overwrite_dupe(self):
        print(
            'Duplicates when using the overwrite in impute_preprocessor_loader'
        )
        # Reset logger instance
        Logger.instance = None
        self.manager.critical_logging_only = False

        # Capture stderr
        old_stderr = sys.stderr
        listener = io.StringIO()
        sys.stderr = listener

        # Do the usual stuff
        overwrite_argument = 'Correct_Overwrite'
        loader = DynamicLoader(
            required_attributes=self.required_attributes,
            path=self.correct_resources
        )
        loader.load_impute_preprocess_modules(
            vep_version=None,
            grch_build=None,
            overwrite=overwrite_argument
        )

        # Get stderr
        out = listener.getvalue()
        sys.stderr = old_stderr

        # Test
        self.assertTrue(
            f"WARNING: Found multiple matches for overwrite "
            f"{overwrite_argument}!" in out)

        # Reset logger to it's original state
        Logger.instance = None
        self.manager.critical_logging_only = True
