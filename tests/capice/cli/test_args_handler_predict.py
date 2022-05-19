import unittest

import pickle
import os
from io import StringIO

from pathlib import Path
from unittest.mock import patch

from molgenis.capice.cli.args_handler_predict import ArgsHandlerPredict
from argparse import ArgumentParser


_project_root_directory = Path(__file__).absolute().parent.parent.parent.parent


class TestArgsHandlerPredict(unittest.TestCase):
    model_path = os.path.join(_project_root_directory,
                              'tests',
                              'resources',
                              'xgb_booster_poc.pickle.dat')

    def setUp(self):
        with open(self.model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_semantic_invalid_version(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '1.0.0-')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model version does not adhere to correct format: 1.0.0-',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_pypi_invalid_prerelease_name(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '1.0.0pre1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model version does not adhere to correct format: 1.0.0pre1',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_major_mismatch(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '2.0.0')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model major version 2.0.0 does not match with CAPICE: 1.0.0!',
                      stderr.getvalue())

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_minor_mismatch(self, pickle_load):
        setattr(self.model, 'CAPICE_version', '1.2.0')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_patch_mismatch(self, pickle_load):
        setattr(self.model, 'CAPICE_version', '1.0.2')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_prerelease_mismatch(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '1.0.0-rc2')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model prerelease version 1.0.0-rc2 does not match with CAPICE: 1.0.0-rc1!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_semantic_prerelease_missing_in_capice(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '1.0.0-rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model prerelease version 1.0.0-rc1 does not match with CAPICE: 1.0.0!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_prerelease_missing_in_model(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '1.0.0')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model prerelease version 1.0.0 does not match with CAPICE: 1.0.0-rc1!',
                      stderr.getvalue())

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0rc1')
    def test_model_pypi_prerelease(self, pickle_load):
        setattr(self.model, 'CAPICE_version', '1.0.0rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_and_pypi_prerelease(self, pickle_load):
        setattr(self.model, 'CAPICE_version', '1.0.0rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_and_pypi_prerelease_mismatch(self, pickle_load, stderr):
        setattr(self.model, 'CAPICE_version', '1.0.0rc2')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model prerelease version 1.0.0rc2 does not match with CAPICE: 1.0.0-rc1!',
                      stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
