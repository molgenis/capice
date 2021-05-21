from src.main.python.resources.errors.errors import ParserError
from src.main.python.core.logger import Logger
import gzip


class CaddHeaderParser:
    """
    Autonomous class to parse just the header of the CADD file to get the CADD version and GRCh build.
    """

    def __init__(self, is_gzipped: bool, cadd_file_loc: str):
        self.log = Logger().logger
        self.log.info('Starting to parse CADD file header.')
        self.is_gzipped = is_gzipped
        self.cadd_file_loc = cadd_file_loc
        self.header = None
        self.header_build = False
        self.header_version = False
        self.header_present = False
        self._parse_header()
        if self.header_present:
            self.log.info("CADD file header successfully identified: {}".format(self.header))
            self._get_header_version_and_grch_build()
        else:
            self.log.warning('Unable to parse CADD file header, header not located. Does the header start with "##"?')

    def _parse_header(self):
        """
        Class to see if the first line is present within the input file.
        """
        if self.is_gzipped:
            with gzip.open(self.cadd_file_loc, mode='rt') as file:
                first_line = file.readline().strip()
        else:
            with open(self.cadd_file_loc, mode='rt') as file:
                first_line = file.readline().strip()
        if first_line.startswith("##"):
            self.header_present = True
            self.header = first_line

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
