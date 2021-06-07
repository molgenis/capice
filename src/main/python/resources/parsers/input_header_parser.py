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
        else:
            self.skip_rows += 1

    def _get_file_type(self):
        if self.header.startswith('## VEP VCF to CAPICE tsv converter'):
            self.file_type = FileType.VEP.value
        elif self.header.startswith('## CADD'):
            self.file_type = FileType.CADD.value
            self._get_header_version_and_grch_build()
        else:
            error_message = 'Unable to recognize origin of input file.'
            self.log.critical(error_message)
            raise InvalidInputFileError(error_message)

    def _get_header_version_and_grch_build(self):
        """
        Class to parse the CADD version and GRCh build present in the header of the CADD output file
        """
        for word in self.header.split(" "):
            if word.upper().startswith('GRCH'):
                self._set_cadd_or_grch_build(current_word=word)

    def _set_cadd_or_grch_build(self, current_word):
        version_and_build = current_word.split("-v")
        for version in version_and_build:
            if version.upper().startswith('GRCH'):
                version = version.upper().strip('GRCH')
                type_of_variable = 'Genome build'
                type_to_convert_to = int
                version = self._try_except_convert_to_type(variable=version,
                                                           type_to_convert_to=type_to_convert_to,
                                                           type_of_variable=type_of_variable)
                self.header_build = version
            else:
                type_of_variable = 'CADD build'
                type_to_convert_to = float
                version = self._try_except_convert_to_type(variable=version,
                                                           type_to_convert_to=type_to_convert_to,
                                                           type_of_variable=type_of_variable)
                self.header_version = version

    def _try_except_convert_to_type(self, variable: any, type_to_convert_to: any, type_of_variable: str):
        try:
            variable = type_to_convert_to(variable)
            self.log.info('CADD file "{}" set to: {}'.format(type_of_variable, variable))
        except ValueError:
            error_message = 'Unable to convert CADD version {} to float.'.format(variable)
            self.log.critical(error_message)
            raise ParserError(error_message)
        return variable

    def get_header_build(self):
        """
        Function to return the parsed CADD header GRCh build
        :return: int
        """
        return self.header_build

    def get_header_version(self):
        """
        Function to return the parsed used CADD version for annotation
        :return: float
        """
        return self.header_version

    def get_header_present(self):
        """
        Function to return the boolean value whenever a header is present within the CADD file
        :return: bool
        """
        return self.header_present

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
