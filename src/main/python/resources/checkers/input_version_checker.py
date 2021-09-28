from src.main.python.core.logger import Logger
from src.main.python.resources.errors.errors import InputError
from src.main.python.core.global_manager import CapiceManager
import warnings


class InputVersionChecker:
    """
    Class to check the given VEP config argument and file VEP version match.

    Class is self running.
    """

    def __init__(self,
                 config_vep_version,
                 file_vep_version,
                 config_grch_build,
                 file_grch_build):
        """
        Class to check the given VEP config argument and
        the header of the VEP file match.
        :param config_vep_version: float or None,
            config argument for the used VEP version
        :param file_vep_version: float or None,
            VEP version according to parsed input file
        :param config_grch_build: int or None,
            config argument for the used GRCh build
        :param file_grch_build: int or None,
            GRCh build according to parsed input file
        """
        self.config_vep_version = config_vep_version
        self.file_vep_version = file_vep_version
        self.config_grch_build = config_grch_build
        self.file_grch_build = file_grch_build
        self.manager = CapiceManager()
        self.export_vep_version = None
        self.export_grch_build = None
        self.check_match = []
        self.unable_check = []
        self.check_overrule = False
        self.log = Logger().logger

        self._run()

    def _run(self):
        """
        Runs checks.
        """
        self._check_all_present()
        if self.check_overrule:
            self._check_overrule()
        self._check_version_match()
        self._set_global_vep_version()
        self._set_global_grch_build()

    def _set_global_vep_version(self):
        """
        Function to provide the CapiceManager with the VEP version to be used
        globally later on in CAPICE.
        """
        self.manager.vep_version = self.export_vep_version
        self.log.info('VEP version set to: {}'.format(self.export_vep_version))

    def _set_global_grch_build(self):
        """
        Function to provide the CapiceManager with the Genome Build version to
        be used globally later on in CAPICE.
        """
        self.manager.grch_build = self.export_grch_build
        self.log.info('GRCh build set to: {}'.format(self.export_grch_build))

    def _check_overrule(self):
        """
        Function called when either the
            VEP version or
            GRCh build
        can not be determined.
        Overrule must be present for both impute and model,
        since it can not determine what file to use without VEP or
        GRCh argument.
        """
        impute = self.manager.overwrite_impute
        model = self.manager.overwrite_model
        if impute is None or len(impute) == 0 and \
                model is None or len(model) == 0:
            error_message = (
                'VEP version or GRCh build not specified and both overwrites are not\n' 
                'set! Not able to find a correct impute or processing file!'
            )
            self.log.critical(error_message)
            raise InputError(error_message)

    def _check_all_present(self):
        """
        Function to check if both the VEP version and GRCh build are present
        within either the config arguments or within the file.
        """
        dict_of_all_present = {
            'VEP': [self.file_vep_version, self.config_vep_version],
            'GRCh': [self.file_grch_build, self.config_grch_build]
        }
        for type_of_check in dict_of_all_present.keys():
            to_check = dict_of_all_present[type_of_check]
            self._check_individual_argument(
                to_check=to_check,
                type_of_check=type_of_check
            )

    def _check_individual_argument(self, to_check, type_of_check):
        """
        Function belonging to _check_all_present to check if a VEP version and
        GRCh build can be set globally.
        :param to_check: list
        :param type_of_check: string
        """
        if None in to_check:
            if to_check.count(None) == len(to_check):
                self._turn_on_check_overrule(type_of_check=type_of_check)
            for argument in to_check:
                self._apply_export_version(argument=argument,
                                           type_of_check=type_of_check)
        else:
            self.check_match.append(type_of_check)

    def _turn_on_check_overrule(self, type_of_check):
        """
        Function to turn on the overrule check if no VEP or GRCh arguments are
        passed.
        """
        self.log.warning(
            f'Unable to obtain {type_of_check} version from file or config file!'
        )
        self.check_overrule = True

    def _apply_export_version(self, argument, type_of_check):
        """
        Function to set the global VEP version or GRCh build.
        :param argument: int or float
        """
        if argument:
            if type_of_check == 'VEP' and argument > 0:
                self.export_vep_version = argument
            elif type_of_check == 'GRCh' and argument > 0:
                self.export_grch_build = argument
            else:
                self.log.warning(
                    f'Encountered an incorrect value for: {type_of_check} '
                    f'({argument})'
                )

    def _check_version_match(self):
        """
        Function to check if the Config Argument and the file header specified
        VEP versions match.
        If not: use the config argument as form of "overwrite" and warn.
        """
        if len(self.check_match) > 0:
            for check_match in self.check_match:
                if check_match == 'VEP':
                    self._check_vep_match(check_match=check_match)
                elif check_match == 'GRCh':
                    self._check_grch_match(check_match=check_match)

    def _check_vep_match(self, check_match):
        if self.file_vep_version != self.config_vep_version:
            self._raise_version_mismatch(type_of_mismatch=check_match,
                                         version_cla=self.file_vep_version,
                                         version_file=self.config_vep_version)
        else:
            self._raise_version_mismatch(type_of_mismatch=check_match,
                                         match_successful=True)
        self.export_vep_version = self.file_vep_version

    def _check_grch_match(self, check_match):
        if self.config_grch_build != self.file_grch_build:
            self._raise_version_mismatch(type_of_mismatch=check_match,
                                         version_cla=self.config_grch_build,
                                         version_file=self.file_grch_build)
        else:
            self._raise_version_mismatch(type_of_mismatch=check_match,
                                         match_successful=True)
        self.export_grch_build = self.file_grch_build

    def _raise_version_mismatch(self, type_of_mismatch, version_cla=None,
                                version_file=None, match_successful=False):
        if match_successful:
            self.log.info(
                'Successfully matched CLA and file versions for {}.'.format(
                    type_of_mismatch
                )
            )
        else:
            warning_message = """
            Warning matching {} versions. 
            CLA version supplied: 
            {} does not match file version: {} !""".format(
                type_of_mismatch,
                version_cla,
                version_file
            ).strip()
            warnings.warn(warning_message)
            self.log.warning(warning_message)
