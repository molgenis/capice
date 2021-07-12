from src.main.python.resources.errors.errors import ParserError, InvalidInputFileError
from src.main.python.core.logger import Logger
from src.main.python.resources.enums.sections import FileType
import gzip


class InputHeaderParser:
    """
    Autonomous class to parse just the header of the input file to get the CADD version and GRCh build (if used
    through the CADD processing pipeline). Also returns the input file type (CADD or VEP).
    """

    def __init__(self, is_gzipped: bool, input_file_loc: str):
        self.log = Logger().logger
        self.log.info('Starting to parse CADD file header.')
        self.is_gzipped = is_gzipped
        self.input_file_loc = input_file_loc
        self.header = None
        self.header_build = False
        self.header_version = False
        self.header_present = False
        self.file_type = None
        self.skip_rows = 0
        self._parse_header()
        if self.header_present:
            self.log.info("Input file header successfully identified: {}".format(self.header))
            self._get_file_type()
        else:
            self.log.warning('Unable to parse input file header, header not located. Does the header start with "##"?')

    def _parse_header(self):
        """
        Class to see if the first line is present within the input file.
        """
        if self.is_gzipped:
            file_handle = gzip.open(self.input_file_loc, mode='rt')
        else:
            file_handle = open(self.input_file_loc, mode='rt')
        for line in file_handle:
            if line.startswith('##'):
                self._add_skip_row(line=line)
            else:
                break
        file_handle.close()

    def _add_skip_row(self, line):
        if self.skip_rows == 0:
            self.header_present = True
            self.header = line
            self.skip_rows += 1
        else:
            self.skip_rows += 1

    def _get_file_type(self):
        if self.header.startswith('## VEP VCF to CAPICE tsv converter'):
            self.file_type = FileType.VEP.value
        else:
            error_message = 'Unable to recognize origin of input file.'
            self.log.critical(error_message)
            raise InvalidInputFileError(error_message)

    def get_skip_rows(self):
        """
        Function to return the integer value of how many rows pandas.read_csv() should skip to reach the data
        :return: int
        """
        return self.skip_rows

    def get_file_type(self):
        """
        Function to return the type of file that was parsed.
        :return: VEP or CADD
        """
        return self.file_type
