from src.errors.errors import InputError, VersionError
from src.data_files.cadd_features import CaddFeatures
from src.utilities.utilities import prepare_dir
from src.global_manager import CapiceManager
import warnings
import sys


class InputChecker:
    def __init__(self, output_loc, log_loc):
        self._check_python_version()
        self.supported_cadd_build = CaddFeatures().\
            supported_cadd_build_genome_builds()
        self.manager = CapiceManager()
        self.output_loc = output_loc
        self.in_log_loc = log_loc
        self.log_loc = None
        self._check_output_loc()
        self._check_log_loc()
        self.manager.set_log_loc(self.log_loc)
        self.genome_build = 37

    def _check_output_loc(self):
        prepare_dir(self.output_loc)

    def _check_log_loc(self):
        if not self.in_log_loc:
            self.log_loc = self.output_loc
        else:
            prepare_dir(self.in_log_loc)
            self.log_loc = self.in_log_loc

    @staticmethod
    def _check_python_version():
        if sys.version_info[0] == 2:
            raise VersionError('Python 2 is not supported.')
        if sys.version_info[1] < 6:
            raise VersionError('Python3.6 must at least be installed.')


    @staticmethod
    def check_input(input_loc):
        """
        Function to check if the input is usable.
        :param input_loc: str, path to CADD annotated file.
        """
        pass

    @staticmethod
    def check_model(model_loc):
        """
        Function to check if the given model loc is usable.
        :param model_loc: str, path to the model.
        """
        pass

    def check_genome_build(self, genome_build):
        """
        Function to check if genome build is supported
        :param genome_build: int
        :return: int
        """
        if not isinstance(genome_build, int):
            raise InputError('Genome build has to be an integer.')

        if genome_build not in self.supported_cadd_build.keys():
            warnings.warn('Genome build {} is not supported, '
                          'switching to build 37.'.format(genome_build))
            return 37
        else:
            self.genome_build = genome_build
            return genome_build

    def check_cadd_build(self, cadd_build):
        """
        Function to check if the CADD file is usable in CAPICE.
        :param cadd_build: float
        :return: float
        """
        if cadd_build not in self.supported_cadd_build[self.genome_build]:
            raise InputError('The combination of CADD version'
                             ' and genome build is not available.')
        # Gotta build in a reader for the cadd file.
        return cadd_build
