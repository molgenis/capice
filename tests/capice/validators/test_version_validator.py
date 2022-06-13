import unittest

from molgenis.capice.validators.version_validator import VersionValidator


class TestVersionValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = VersionValidator()

    def test_capice_semantic_invalid_version(self):
        """
        Tests if ValueError is raised when CAPICE does not adhere to the semantic versioning
        """
        version = '1.0.0-'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_capice_version(version)
        self.assertEqual(
            'CAPICE version does not adhere to correct format: 1.0.0-', str(cm.exception)
        )

    def test_model_semantic_invalid_version(self):
        """
        Tests if ValueError is raised when the model does not adhere to the semantic versioning
        """
        version = '1.0.0-'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_model_version(version)
        self.assertEqual(
            'Model version does not adhere to correct format: 1.0.0-', str(cm.exception)
        )

    def test_capice_pep440_invalid_prerelease_name(self):
        """
        Tests if ValueError is raised when CAPICE does not adhere to the PEP440 prerelease
        nomenclature.

        See also: https://peps.python.org/pep-0440/#pre-releases
        """
        version = '1.0.0pre1'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_capice_version(version)
        self.assertEqual(
            'CAPICE version does not adhere to correct format: 1.0.0pre1', str(cm.exception)
        )

    def test_model_pep440_invalid_prerelease_name(self):
        """
        Tests if ValueError is raised when the model does not adhere to the PEP440 prerelease
        nomenclature.

        See also: https://peps.python.org/pep-0440/#pre-releases
        """
        version = '1.0.0pre1'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_model_version(version)
        self.assertEqual(
            'Model version does not adhere to correct format: 1.0.0pre1', str(cm.exception)
        )

    def test_major_mismatch(self):
        """
        Tests if ValueError is raised when the model and framework mismatch in MAJOR versions.
        """
        version_capice = '3.0.0'
        version_model = '2.0.0'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE major version 3.0.0 does not match with the model 2.0.0!', str(cm.exception)
        )

    def test_minor_mismatch(self):
        """
        Tests if no error is raised when testing 2 different minor versions (major still matches).
        """
        version_capice = '3.2.0'
        version_model = '3.0.0'
        self.validator.validate_versions_compatible(version_capice, version_model)

    def test_patch_mismatch(self):
        """
        Tests if no error is raised when testing 2 different patch versions (major still matches).
        """
        version_capice = '3.0.1'
        version_model = '3.0.0'
        self.validator.validate_versions_compatible(version_capice, version_model)

    def test_semantic_prerelease_mismatch(self):
        """
        Tests if ValueError is raised when testing 2 different prerelease versions.
        """
        version_capice = '4.0.0-rc1'
        version_model = '4.0.0-rc2'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE prerelease version 4.0.0-rc1 does not match the model prerelease version '
            '4.0.0-rc2 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_semantic_prerelease_with_minor_mismatch(self):
        """
        Tests if ValueError is raised when testing 2 same prerelease versions, but at different
        minor versions.
        """
        version_capice = '4.0.0-rc1'
        version_model = '4.2.0-rc1'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE minor version 4.0.0-rc1 does not match the model minor version '
            '4.2.0-rc1 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_semantic_prerelease_with_patch_mismatch(self):
        """
        Tests if ValueError is raised when testing 2 same prerelease versions, but at different
        patch versions.
        """
        version_capice = '4.0.0-rc1'
        version_model = '4.0.2-rc1'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE patch version 4.0.0-rc1 does not match the model patch version '
            '4.0.2-rc1 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_semantic_prerelease_missing_capice(self):
        """
        Tests if ValueError is raised when the model has a prerelease, but CAPICE does not.
        """
        version_capice = '4.0.0'
        version_model = '4.0.0-rc1'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE prerelease version 4.0.0 does not match the model prerelease version '
            '4.0.0-rc1 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_semantic_prerelease_missing_model(self):
        """
        Tests if ValueError is raised when the CAPICE has a prerelease, but the model does not.
        """
        version_capice = '4.0.0-rc1'
        version_model = '4.0.0'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE prerelease version 4.0.0-rc1 does not match the model prerelease version '
            '4.0.0 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_pep440_prerelease_missing_capice(self):
        """
        Tests if ValueError is raised when the model has a prerelease, but CAPICE does not. In
        PEP440 format.
        """
        version_capice = '4.0.0'
        version_model = '4.0.0rc1'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE prerelease version 4.0.0 does not match the model prerelease version '
            '4.0.0rc1 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_pep440_prerelease_missing_model(self):
        """
        Tests if ValueError is raised when CAPICE has a prerelease, but the model does not. In
        PEP440 format.
        """
        version_capice = '4.0.0rc1'
        version_model = '4.0.0'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE prerelease version 4.0.0rc1 does not match the model prerelease version '
            '4.0.0 (should match for pre-releases)!',
            str(cm.exception)
        )

    def test_pep440_prerelease_match(self):
        """
        Tests if no ValueError is raised when the model and CAPICE match in prerelease,
        but in PEP440 format.
        """
        version_capice = '4.0.0rc1'
        version_model = '4.0.0rc1'
        self.validator.validate_versions_compatible(version_capice, version_model)

    def test_pep440_semantic_prerelease_match(self):
        """
        Tests if no ValueError is raised when the model and CAPICE match in prerelease,
        but the CAPICE version is in PEP440 and the model is in semantic.
        """
        version_capice = '4.0.0rc1'
        version_model = '4.0.0-rc1'
        self.validator.validate_versions_compatible(version_capice, version_model)

    def test_pep440_semantic_prerelease_mismatch(self):
        """
        Tests if ValueError is raised when the model and CAPICE do not match in prerelease,
        but the CAPICE version is in PEP440 and the model is in semantic.
        """
        version_capice = '4.0.0rc1'
        version_model = '4.0.0-rc2'
        with self.assertRaises(ValueError) as cm:
            self.validator.validate_versions_compatible(version_capice, version_model)
        self.assertEqual(
            'CAPICE prerelease version 4.0.0rc1 does not match the model prerelease version '
            '4.0.0-rc2 (should match for pre-releases)!',
            str(cm.exception)
        )


if __name__ == '__main__':
    unittest.main()
