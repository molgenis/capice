from src.main.python.core.logger import Logger
from src.main.python.resources.errors.errors import InputError
from src.main.python.core.global_manager import CapiceManager
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
        self.check_match = []
        self.unable_check = []
        self.check_overrule = False
        self.log = Logger().logger
        self._check_all_present()
        if self.check_overrule:
            self._check_overrule()
        self._check_version_match()
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
        """
        Function called when either the CADD version or GRCh build can not be determined. Overrule must be present
        for both impute and model, since it can not determine what file to use without CADD or GRCh argument.
        """
        if self.manager.overwrite_impute is False and self.manager.overwrite_model is False:
            error_message = 'CADD version or GRCh build not specified and both overwrites are not set! ' \
                            'Not able to find a correct impute or processing file!'
            self.log.critical(error_message)
            raise InputError(error_message)

    def _check_all_present(self):
        """
        Function to check if both the CADD version and GRCh build are present within either the command line
        arguments or within the file.
        """
        dict_of_all_present = {
            'CADD': [self.cla_cadd_version, self.file_cadd_version],
            'GRCh': [self.cla_grch_build, self.file_grch_build]
        }
        for type_of_check in dict_of_all_present.keys():
            to_check = dict_of_all_present[type_of_check]
            if False in to_check:
                if to_check.count(False) == len(to_check):
                    self.check_overrule = type_of_check
                    self.log.warning('Unable to obtain {} version from file or command line!'.format(type_of_check))
                    self.check_overrule = True
                for argument in to_check:
                    if argument is not False:
                        if type_of_check == 'CADD':
                            self.export_cadd_version = argument
                        else:
                            self.export_grch_build = argument
            else:
                self.check_match.append(type_of_check)

    def _check_version_match(self):
        """
        Function to check if the Command Line Argument and the file header specified CADD versions match.
        If not: use the command line argument as form of "overwrite" and warn.
        """
        if len(self.check_match) > 0:
            for check_match in self.check_match:
                if check_match == 'CADD':
                    if self.cla_cadd_version != self.file_cadd_version:
                        self._raise_version_mismatch(type_of_mismatch=check_match,
                                                     version_cla=self.cla_cadd_version,
                                                     version_file=self.file_cadd_version)
                    else:
                        self._raise_version_mismatch(type_of_mismatch=check_match,
                                                     match_successful=True)
                    self.export_cadd_version = self.cla_cadd_version
                else:
                    if self.cla_grch_build != self.file_grch_build:
                        self._raise_version_mismatch(type_of_mismatch=check_match,
                                                     version_cla=self.cla_grch_build,
                                                     version_file=self.file_grch_build)
                    else:
                        self._raise_version_mismatch(type_of_mismatch=check_match,
                                                     match_successful=True)
                    self.export_grch_build = self.cla_grch_build

    def _raise_version_mismatch(self, type_of_mismatch, version_cla=None, version_file=None, match_successful=False):
        if match_successful:
            self.log.info('Successfully matched CLA and file versions for {}.'.format(type_of_mismatch))
        else:
            warning_message = "Warning matching {} versions. " \
                              "CLA version supplied: {} does not match file version: {} !".format(type_of_mismatch,
                                                                                                  version_cla,
                                                                                                  version_file)
            warnings.warn(warning_message)
            self.log.warning(warning_message)
