import os
import unittest

from molgenis.capice.validators.input_validator import InputValidator
from tests.capice.test_templates import _project_root_directory, ResourceFile, FakeResourceFile


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

    def test_create_output_path(self):
        print('Creating output location')
        with self.assertWarns(Warning):
            self.input_validator.validate_output_path(self.new_directory)
        self.assertTrue(
            self.new_directory_name in os.listdir(_project_root_directory)
        )

    def test_input_single_extension(self):
        allowed_extensions = ('.tsv.gz',)
        self.input_validator.validate_input_path(ResourceFile.PREDICT_INPUT_TSV_GZ.value,
                                                 extension=allowed_extensions)

    def test_input_multiple_extensions(self):
        allowed_extensions = ('.tsv', '.tsv.gz')
        self.input_validator.validate_input_path(ResourceFile.PREDICT_INPUT_TSV_GZ.value,
                                                 extension=allowed_extensions)

    def test_input_multiple_extensions_invalid(self):
        allowed_extensions = ('.tsv', '.tsv.gz')
        with self.assertRaises(IOError) as e:
            self.input_validator.validate_input_path(ResourceFile.XGB_BOOSTER_POC_UBJ.value,
                                                     extension=allowed_extensions)

        self.assertEqual(f'{ResourceFile.XGB_BOOSTER_POC_UBJ.value} does not exist!',
                         e.exception.strerror)

    def test_input_multiple_extensions_invalid(self):
        allowed_extensions = ('.tsv', '.tsv.gz')
        with self.assertRaises(IOError) as e:
            self.input_validator.validate_input_path(ResourceFile.XGB_BOOSTER_POC_UBJ.value,
                                                     extension=allowed_extensions)

        self.assertEqual(f'{ResourceFile.XGB_BOOSTER_POC_UBJ.value} does not match required '
                         f'extension: .tsv, .tsv.gz',
                         str(e.exception))

    def test_input_non_existing(self):
        allowed_extensions = ('.tsv', '.tsv.gz')
        with self.assertRaises(FileNotFoundError) as e:
            self.input_validator.validate_input_path(FakeResourceFile.PREDICT_INPUT_TSV_GZ.value,
                                                     extension=allowed_extensions)

        self.assertEqual(f'{FakeResourceFile.PREDICT_INPUT_TSV_GZ.value} does not exist!',
                         str(e.exception))


if __name__ == '__main__':
    unittest.main()
