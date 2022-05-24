import unittest
from unittest.mock import patch

import os
import pickle
from io import StringIO
from argparse import ArgumentParser

from tests.capice.test_templates import _project_root_directory
from molgenis.capice.cli.args_handler_predict import ArgsHandlerPredict


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
        """
        Tests invalid semantic version that contains a '-' without pre-release text behind it
        (no empty identifier allowed).

        See also: https://semver.org/#spec-item-9
        """
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
    def test_model_pep440_invalid_prerelease_name(self, pickle_load, stderr):
        """
        Tests invalid PEP version as pre-release format is very strict (a/b/rc<int> only).

        See also: https://peps.python.org/pep-0440/#pre-releases
        """
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
        """
        Tests major version mismatch between CAPICE & model (should exit).
        """
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
        """
        Tests minor version mismatch between CAPICE & model (should not exit).
        """
        setattr(self.model, 'CAPICE_version', '1.2.0')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_patch_mismatch(self, pickle_load):
        """
        Tests patch version mismatch between CAPICE & model (should not exit).
        """
        setattr(self.model, 'CAPICE_version', '1.0.2')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_prerelease_mismatch(self, pickle_load, stderr):
        """
        Tests pre-release mismatch if rest of version is identical (should exit).
        """
        setattr(self.model, 'CAPICE_version', '1.0.0-rc2')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model pre-release version 1.0.0-rc2 does not match with CAPICE: 1.0.0-rc1!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_prerelease_with_minor_mismatch(self, pickle_load, stderr):
        """
        Tests that for identical pre-release text but differing minor version, CAPICE exits.

        If 2 different pre-release versions within the same patch version should already fail
        due to instability between pre-release versions, it should not be possible to use a
        pre-release from a different major/minor/patch version either.
        """
        setattr(self.model, 'CAPICE_version', '1.2.0-rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model minor version 1.2.0-rc1 does not match with CAPICE: 1.0.0-rc1 '
                      '(should match for pre-releases)!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_prerelease_with_patch_mismatch(self, pickle_load, stderr):
        """
        Tests that for identical pre-release text but differing patch version, CAPICE exits.

        If 2 different pre-release versions within the same patch version should already fail
        due to instability between pre-release versions, it should not be possible to use a
        pre-release from a different major/minor/patch version either.
        """
        setattr(self.model, 'CAPICE_version', '1.0.2-rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model patch version 1.0.2-rc1 does not match with CAPICE: 1.0.0-rc1 '
                      '(should match for pre-releases)!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0')
    def test_model_semantic_prerelease_missing_in_capice(self, pickle_load, stderr):
        """
        Tests if pre-release model (using semantic version formatting) in combination with final
        CAPICE version exits.

        If either CAPICE or model uses a pre-release version, both should contain pre-release text
        so that non-pre-release code/model is not used in combination with pre-release model/code
        due to instability of pre-releases.
        """
        setattr(self.model, 'CAPICE_version', '1.0.0-rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model pre-release version 1.0.0-rc1 does not match with CAPICE: 1.0.0!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_prerelease_missing_in_model(self, pickle_load, stderr):
        """
        Tests if pre-release CAPICE (using semantic version formatting) in combination with final
        model version exits.

        If either CAPICE or model uses a pre-release version, both should contain pre-release text
        so that non-pre-release code/model is not used in combination with pre-release model/code
        due to instability of pre-releases.
        """
        setattr(self.model, 'CAPICE_version', '1.0.0')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model pre-release version 1.0.0 does not match with CAPICE: 1.0.0-rc1!',
                      stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0rc1')
    def test_model_pep440_prerelease_missing_in_model(self, pickle_load, stderr):
        """
        Tests if pre-release CAPICE (using PEP 440 version formatting) in combination with final
        model version exits.

        If either CAPICE or model uses a pre-release version, both should contain pre-release text
        so that non-pre-release code/model is not used in combination with pre-release model/code
        due to instability of pre-releases.
        """
        setattr(self.model, 'CAPICE_version', '1.0.0')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model pre-release version 1.0.0 does not match with CAPICE: 1.0.0rc1!',
                      stderr.getvalue())

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0rc1')
    def test_model_pep440_prerelease(self, pickle_load):
        """
        Tests identical pre-release version using PEP 440 (should not exit).
        """
        setattr(self.model, 'CAPICE_version', '1.0.0rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_and_pep440_prerelease(self, pickle_load):
        """
        Tests identical pre-release version where formatting differs but portrays same version
        (should not exit).

        While the actual string differs, the portrayed version is identical and therefore should
        not fail.
        """
        setattr(self.model, 'CAPICE_version', '1.0.0rc1')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        args_handler.validate_model(self.model_path)

    @patch('sys.stderr', new_callable=StringIO)
    @patch.object(pickle, 'load')
    @patch('molgenis.capice.cli.args_handler_predict.__version__', '1.0.0-rc1')
    def test_model_semantic_and_pep440_prerelease_mismatch(self, pickle_load, stderr):
        """
        Tests mismatch in pre-release version when using differing formatting (CAPICE=semantic,
        model=PEP 440). Should exit.

        While the Strings differ, the comparison should be made based on an actual version number
        difference and therefore the error message is validated so that CAPICE is exited for the
        right reason.
        """
        setattr(self.model, 'CAPICE_version', '1.0.0rc2')
        pickle_load.return_value = self.model

        args_handler = ArgsHandlerPredict(ArgumentParser())
        with self.assertRaises(SystemExit) as cm:
            args_handler.validate_model(self.model_path)

        self.assertEqual(cm.exception.code, 2)
        self.assertIn('Model pre-release version 1.0.0rc2 does not match with CAPICE: 1.0.0-rc1!',
                      stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
