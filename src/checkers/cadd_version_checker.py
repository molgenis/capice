from src.logger import Logger
from src.errors.errors import InputError
from src.global_manager import CapiceManager
import warnings


class CaddVersionChecker:
    """
    Class to check the given CADD command line arguments and the header of the CADD file

    Class is self running thanks to the init, no function has to be called externally.
    """
    def __init__(self,
                 cla_cadd_version: float,
                 cla_grch_build: int,
                 file_cadd_version: float,
                 file_grch_build: int):
        """
        Class to check the given CADD command line arguments and the header of the CADD file
        :param cla_cadd_version: float, command line argument for the used CADD version
        :param cla_grch_build: int, command line argument for the used GRCh build
        :param file_cadd_version: float, the CADD version present in the header of the CADD file
        :param file_grch_build: int, the GRCh build present in the header of the CADD file
        """
        self.cla_cadd_version = cla_cadd_version
        self.cla_grch_build = cla_grch_build
        self.file_cadd_version = file_cadd_version
        self.file_grch_build = file_grch_build
        self.manager = CapiceManager()
        self.export_cadd_version = None
        self.export_grch_build = None
        self.check_match_versions = True
        self.check_match_builds = True
        self.check_overrule = False
        self.log = Logger().logger
        self._check_all_version_present()
        self._check_all_builds_present()
        if self.check_overrule:
            self._check_overrule()
        self._check_version_match()
        self._check_grch_build_match()
        self._set_global_cadd_version()
        self._set_global_grch_build()

    def _set_global_cadd_version(self):
        """
        Function to provide the CapiceManager with the cadd version to be used globally later on in CAPICE.
        """
        self.manager.cadd_version = self.export_cadd_version
        self.log.info('CADD version set to: {}'.format(self.export_cadd_version))

    def _set_global_grch_build(self):
        """
        Function to provide the CapiceManager with the Genome Build version to be used globally later on in CAPICE.
        """
        self.manager.grch_build = self.export_grch_build
        self.log.info('GRCh build set to: {}'.format(self.export_grch_build))

    def _check_overrule(self):
        if self.manager.overwrite_impute is False and self.manager.overwrite_model is False:
            error_message = 'CADD version or GRCh build not specified and both overwrites are not set! ' \
                            'Not able to find a correct impute or processing file!'
            self.log.critical(error_message)
            raise InputError(error_message)

    def _check_all_version_present(self):
        """
        Function to check if both the command line argument and the file CADD versions are present.
        If only 1 is present, set the export CADD version to it.
        If none is present, raise InputError.
        """
        list_of_cadd_versions = [self.cla_cadd_version, self.file_cadd_version]
        if None in list_of_cadd_versions:
            if list_of_cadd_versions.count(None) == len(list_of_cadd_versions):
                self.check_overrule = True
                self.log.warning('No CADD version defined!')
            self.check_match_versions = False
            for version in list_of_cadd_versions:
                if version is not None:
                    self.export_cadd_version = version

    def _check_all_builds_present(self):
        """
        Function to check if both the command line argument and the file GRCh build are present.
        If only 1 is present, set the export GRCh build to it.
        If none is present, raide InputError.
        """
        list_of_cadd_grch_builds = [self.cla_grch_build, self.file_grch_build]
        if None in list_of_cadd_grch_builds:
            if list_of_cadd_grch_builds.count(None) == len(list_of_cadd_grch_builds):
                self.check_overrule = True
                self.log.warning('No CADD GRCh build defined!')
            self.check_match_builds = False
            for build in list_of_cadd_grch_builds:
                if build is not None:
                    self.export_grch_build = build

    def _check_version_match(self):
        """
        Function to check if the Command Line Argument and the file header specified CADD versions match.
        If not: use the command line argument as form of "overwrite" and warn.
        """
        if self.check_match_versions:
            if self.cla_cadd_version != self.file_cadd_version:
                warning_message = "Version supplied on the command line:" \
                                  " {} does not match the CADD file version: {}!".format(
                                    self.cla_cadd_version,
                                    self.file_cadd_version
                                    )
                warnings.warn(warning_message)
                self.log.warning(warning_message)
            else:
                self.log.info('CADD versions from the command line and file match.')
            self.export_cadd_version = self.cla_cadd_version

    def _check_grch_build_match(self):
        """
        Function to check if the Command Line Argument and the file specified GRCh build match.
        If not: use the CLA argument as form of "overwrite" and warn.
        """
        if self.check_match_builds:
            if self.cla_grch_build != self.file_grch_build:
                warning_message = "GRCh build supplied on the command line:" \
                                  " {} does not match the CADD file GRCh build: {}!".format(
                                    self.cla_cadd_version,
                                    self.file_cadd_version
                                    )
                warnings.warn(warning_message)
                self.log.warning(warning_message)
            else:
                self.log.info('GRCh builds from the command line and file match.')
            self.export_grch_build = self.cla_grch_build
