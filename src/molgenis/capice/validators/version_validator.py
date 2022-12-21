import re
from re import match

from molgenis.capice.utilities.enums import Versioning


class VersionValidator:
    def __init__(self):
        self.regex = Versioning.VALIDATION_REGEX.value

    def validate_capice_version(self, capice_version: str):
        """
        Validates if the CAPICE version adheres CAPICE versioning standards, which originate from
        the Semantic versioning standards.

        For instance:
        3.0.0
        3.1.0
        3.1.1
        3.1.1-rc1
        3.1.1rc1
        Are all valid versions.

        Parameters
        ----------
        capice_version : str
            The version of the CAPICE framework.

        Raises
        ------
        ValueError
            Raised when the CAPICE framework version does not adhere to the versioning standards.
        """
        if match(self.regex, capice_version) is None:
            raise ValueError(f'CAPICE version does not adhere to correct format: {capice_version}')

    def validate_model_version(self, model_version: str):
        """
        Validates if the model version adheres CAPICE versioning standards, which originate from
        the Semantic versioning standards.

        For instance:
        3.0.0
        3.1.0
        3.1.1
        3.1.1-rc1
        3.1.1rc1
        Are all valid versions.

        Parameters
        ----------
        model_version : str
            The version of the CAPICE model.

        Raises
        ------
        ValueError
            Raised when the model version does not adhere to the versioning standards.
        """
        if match(self.regex, model_version) is None:
            raise ValueError(f'Model version does not adhere to correct format: {model_version}')

    def validate_versions_compatible(self, capice_version: str, model_version: str):
        """
        Validates if the model version and the CAPICE framework versions are compatible with each
        other.

        Parameters
        ----------
        capice_version : str
            The version of the CAPICE framework.


        model_version : str
            The version of the CAPICE model.

        Raises
        ------
        ValueError
            Raised when the model and framework versions are not compatible.
        """
        # All mypy ignores here are because attributes are not found.
        capice = match(self.regex, capice_version)
        model = match(self.regex, model_version)
        if capice.group('major') != model.group('major'):  # type: ignore
            raise ValueError(
                f'CAPICE major version {capice.string} '  # type: ignore
                f'does not match with the model '
                f'{model.string}!'  # type: ignore
            )

        if capice.group('prerelease') or model.group('prerelease'):  # type: ignore
            self._validate_prerelease(capice, model)  # type: ignore

    @staticmethod
    def _validate_prerelease(capice_version: re.Match,
                             model_version: re.Match):
        matches = ['minor', 'patch', 'prerelease']
        for m in matches:
            if capice_version.group(m) != model_version.group(m):
                raise ValueError(
                    f'CAPICE {m} version {capice_version.string} does not match the model {m} '
                    f'version {model_version.string} (should match for pre-releases)!'
                )
