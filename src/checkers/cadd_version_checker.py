from src.logger import Logger
from src.errors.errors import InputError
from src.global_manager import CapiceManager
import warnings


class CaddVersionChecker:
    """
    Class to check the given CADD command line arguments and the header of the CADD file
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
        self.log = Logger().get_logger()
        self._check_all_version_present()
        self._check_all_builds_present()
        self._check_version_match()
        self._check_grch_build_match()
        self._set_global_cadd_version()
        self._set_global_grch_build()

    def _set_global_cadd_version(self):
        self.manager.set_cadd_version(cadd_version=self.export_cadd_version)
        self.log.info('CADD version set to: {}'.format(self.export_cadd_version))

    def _set_global_grch_build(self):
        self.manager.set_grch_build(grch_build=self.export_grch_build)
        self.log.info('GRCh build set to: {}'.format(self.export_grch_build))

    def _check_all_version_present(self):
        list_of_cadd_versions = [self.cla_cadd_version, self.file_cadd_version]
        if None in list_of_cadd_versions:
            if list_of_cadd_versions.count(None) == len(list_of_cadd_versions):
                self.log.critical('No CADD version defined!')
                raise InputError('No CADD version defined!')
            self.check_match_versions = False
            for version in list_of_cadd_versions:
                if version:
                    self.export_cadd_version = version

    def _check_all_builds_present(self):
        list_of_cadd_grch_builds = [self.cla_grch_build, self.file_grch_build]
        if None in list_of_cadd_grch_builds:
            if list_of_cadd_grch_builds.count(None) == len(list_of_cadd_grch_builds):
                self.log.critical('No CADD GRCh build defined!')
                raise InputError('No CADD GRCh build defined!')
            self.check_match_builds = False
            for build in list_of_cadd_grch_builds:
                if build:
                    self.export_grch_build = build

    def _check_version_match(self):
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
