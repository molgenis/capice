import unittest

import os
import pickle

from src.molgenis.capice import __version__
from tests.capice.test_templates import _project_root_directory
from molgenis.capice.validators.version_validator import VersionValidator


class TestResources(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = VersionValidator()

    def test_resource_model(self):
        """
        Test that the resources model is valid with the current CAPICE version.
        """
        model_path = os.path.join(_project_root_directory, 'tests', 'resources',
                                  'xgb_booster_poc.pickle.dat')
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        self.validator.validate_model_version(model.CAPICE_version)
        self.validator.validate_versions_compatible(__version__, model.CAPICE_version)


if __name__ == '__main__':
    unittest.main()
