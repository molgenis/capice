import unittest

import os
import pickle
from re import match

from src.molgenis.capice import __version__
from molgenis.capice.utilities.enums import Versioning
from tests.capice.test_templates import _project_root_directory


class TestResources(unittest.TestCase):
    def test_resource_model(self):
        """
        Test that the resources model is valid with the current CAPICE version.
        """
        model_path = os.path.join(_project_root_directory, 'tests', 'resources',
                                  'xgb_booster_poc.pickle.dat')
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        model_version = match(Versioning.VALIDATION_REGEX.value, model.CAPICE_version)
        if model_version is None:
            raise ValueError('PoC model has an incorrect version format!')
        capice_version = match(Versioning.VALIDATION_REGEX.value, __version__)
        if model_version.group('major') != capice_version.group('major'):
            raise ValueError('PoC model major version does not match!')
        if model_version.group('prerelease') or capice_version.group('prerelease'):
            if model_version.group('minor') != capice_version.group('minor') or \
                    model_version.group('patch') != capice_version.group('patch') or \
                    model_version.group('prerelease') != capice_version.group('prerelease'):
                raise ValueError('PoC prerelease model does not match CAPICE prerelease model!')


if __name__ == '__main__':
    unittest.main()
