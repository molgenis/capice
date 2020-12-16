from src.errors.errors import VersionError, InputError
from src.utilities.utilities import prepare_dir, check_dir_exists, check_file_exists
import warnings
import sys


class InputChecker:
    """
    Checker for the remaining supplied arguments
    """
    def __init__(self):
        self.input_loc = None
        self.output_loc = None
        self.cadd_build_input = None
        self.genome_build_input = None

    def check_arguments(self,
                        input_loc: str,
                        output_loc: str):
        """
        Function to check if the input is usable.
        :param input_loc: str, path to CADD annotated file.
        :param output_loc: str, path to export files to.
        :returns input_loc, output_loc
        """
        self.input_loc = input_loc
        self.output_loc = output_loc
        self._check_input_loc()
        self._check_output_loc()

    def _check_input_loc(self):
        if not check_file_exists(self.input_loc):
            raise InputError("Input file does not exist!")

    def _check_output_loc(self):
        if not check_dir_exists(self.output_loc):
            warnings.warn("Output directory does not exist, creating.")
            prepare_dir(self.output_loc)


class LogChecker:
    """
    Initial check of the arguments for the logger.
    """
    def __init__(self, log_loc: str, output_loc: str, verbose: bool):
        self._check_python_version()
        self.log_loc = log_loc
        self.output_loc = output_loc
        self.verbose = verbose

    @staticmethod
    def _check_python_version():
        if sys.version_info[0] == 2:
            raise VersionError('Python 2 is not supported.')
        if sys.version_info[1] < 6:
            raise VersionError('Python3.6 must at least be installed.')

    def check_log_loc(self):
        """
        Check both the log_loc and output_loc if they are valid
        :return: path-like, the directory to put the log file in
        """
        log_loc = None
        if self.log_loc:
            if not check_dir_exists(self.log_loc):
                warnings.warn("Output location {} not found, creating.".format(self.log_loc))
                prepare_dir(self.log_loc)
                log_loc = self.log_loc
        else:
            if not check_dir_exists(self.output_loc):
                warnings.warn("Output location {} not found, creating.".format(self.output_loc))
                prepare_dir(self.output_loc)
                log_loc = self.output_loc
        return log_loc

    def _check_verbose(self):
        if not isinstance(self.verbose, bool):
            raise InputError("Verbose level must a boolean.")
