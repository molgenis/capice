from src.errors.errors import VersionError, InputError
from src.utilities.utilities import prepare_dir
from src.global_manager import CapiceManager
import sys
import gzip


class InputChecker:
    def __init__(self, output_loc, log_loc):
        self._check_python_version()
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

    def check_cadd_header(self,
                          input_loc: str,
                          cadd_build_input,
                          genome_build_input):
        """
        Function to check if the input is usable.
        :param input_loc: str, path to CADD annotated file.
        :param cadd_build_input: boolean or command line input of -cb
        :param genome_build_input: boolean or command line input of -gb
        """
        if not cadd_build_input or not genome_build_input:
            if input_loc.endswith('.gz'):
                with gzip.open(input_loc, 'rb') as input_file:
                    cadd_header = input_file.readlines(1)[0].decode()
            else:
                with open(input_loc, 'r') as input_file:
                    cadd_header = input_file.readlines(1)[0]
            self._check_cadd_header(cadd_header, cadd_build_input)

    @staticmethod
    def _check_cadd_header(cadd_header, cadd_build_input):
        if not cadd_header.startswith('##CADD'):
            if not cadd_build_input:
                raise InputError(
                    'Unable to read CADD version from CADD file.'
                )
            else:
                raise InputError(
                    'Unable to read GRCh version from CADD file.'
                )
