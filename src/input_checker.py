from src.errors.errors import VersionError, InputError
from src.utilities.utilities import prepare_dir, check_dir_exists, check_file_exists
import warnings
import sys


class InputChecker:
    """
    Checker for the remaining supplied arguments
    """

    @staticmethod
    def check_input_loc(input_loc):
        """
        Function to check if there is a file at the input location
        :param input_loc: full path to input file
        """
        if not check_file_exists(input_loc):
            raise InputError("Input file does not exist!")

    @staticmethod
    def check_output_loc(output_loc):
        """
        Function to check if the output directory exists and, if not, make it.
        :param output_loc: path to output folder
        """
        if not check_dir_exists(output_loc):
            warnings.warn("Output directory does not exist, creating.")
            prepare_dir(output_loc)


class LogChecker:
    """
    Initial check of the arguments for the logger.
    """
    def __init__(self, log_loc: str, output_loc: str):
        self._check_python_version()
        self.log_loc = log_loc
        self.output_loc = output_loc

    @staticmethod
    def _check_python_version():
        """
        Check if the python version is at least 3.0.0
        """
        if sys.version_info[0] == 2:
            raise VersionError('Python 2 is not supported.')
        if sys.version_info[1] < 6:
            raise VersionError('Python3.6 must at least be installed.')

    def check_log_loc(self):
        """
        Check both the log_loc and output_loc if they are valid
        :return: path-like, the directory to put the log file in
        """
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
