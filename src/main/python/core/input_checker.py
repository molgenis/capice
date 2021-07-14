from src.main.python.resources.errors.errors import InputError
from src.main.python.resources.utilities.utilities import prepare_dir, check_dir_exists, check_file_exists, \
    get_filename_and_extension
import warnings
import os


class InputChecker:
    """
    Checker for the remaining supplied arguments
    """

    def __init__(self):
        self.output_filename = ''
        self.output_directory = ''

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

    def check_input_output_directories(self, input_path, output_path):
        """
        Function to check the input location, output location and will provide
        :param input_path:
        :param output_path:
        :return:
        """
        if output_path is None:
            self._create_capice_output_filename(input_path=input_path)
        else:
            # Check if it is a path or else just a filename
            if len(os.path.dirname(output_path)) > 0:
                # Then I know it's an output filepath + possibly name
                if os.path.splitext(output_path)[1] != '':
                    # Then I know it is a full path + filename
                    self._create_capice_output_filename(input_path=output_path, append_capice=False)
                else:
                    # Then I know it's a full path
                    self._create_capice_output_filename(input_path=input_path, output_path=output_path, ispath=True)
            else:
                # Then I know it's an output filename
                self.output_directory = os.path.dirname(input_path)
                self.output_filename = output_path
        self._check_gzip_extension()

    def _create_capice_output_filename(self, input_path, output_path=None, append_capice=True, ispath=False):
        if output_path is None:
            output_path = input_path
        input_filename, extension = get_filename_and_extension(input_path)
        if append_capice:
            self.output_filename = '{}_capice.{}'.format(input_filename, extension)
        else:
            self.output_filename = '{}.{}'.format(input_filename, extension)
        if ispath:
            self.output_directory = output_path
        else:
            self.output_directory = os.path.dirname(output_path)

    def _check_gzip_extension(self):
        if not self.output_filename.endswith('.gz'):
            self.output_filename = self.output_filename + '.gz'

    @staticmethod
    def check_reference(reference):
        """
        Function to check if the reference files exist
        """
        locs = [reference, '{}.{}'.format(reference, 'fai')]
        for loc in locs:
            if loc is False or not check_file_exists(loc):
                raise FileNotFoundError('Unable to locate all required files to annotate through the CADD database.')

    def get_output_filename(self):
        return self.output_filename

    def get_output_directory(self):
        return self.output_directory


class LogChecker:
    """
    Initial check of the arguments for the logger.
    """

    def __init__(self, log_loc: [str, None], output_loc: str):
        self.log_loc = log_loc
        self.output_loc = output_loc

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
