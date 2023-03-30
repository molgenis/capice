import unittest

from molgenis.capice import __version__
from tests.capice.test_templates import ResourceFile, load_model
from molgenis.capice.validators.version_validator import VersionValidator


class TestResources(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = VersionValidator()

    def test_resource_model(self):
        """
        Test that the resources model is valid with the current CAPICE version.
        """
        model = load_model(ResourceFile.XGB_BOOSTER_POC_JSON.value)
        self.validator.validate_model_version(model.CAPICE_version)
        self.validator.validate_versions_compatible(__version__, model.CAPICE_version)


if __name__ == '__main__':
    unittest.main()
