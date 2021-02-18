from src.errors.errors import ParserError
from src.logger import Logger
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
        self.header_build = None
        self.header_version = None
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
            with open(self.cadd_file_loc) as file:
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
                version_and_build = word.split("-v")
                for version_build in version_and_build:
                    if version_build.upper().startswith('GRCH'):
                        version_build = version_build.upper().strip('GRCH')
                        try:
                            self.header_build = int(version_build)
                            self.log.info('CADD file header genome build GRCh set to: {}'.format(self.header_build))
                        except ValueError:
                            self.log.error('Unable to convert CADD genome build {} to integer.'.format(version_build))
                            raise ParserError(
                                "Could not convert header CADD version (type = {}) to integer.".format(
                                    type(version_build)))
                    else:
                        try:
                            self.header_version = float(version_build)
                            self.log.info('CADD file header used CADD version set to: {}'.format(self.header_version))
                        except ValueError:
                            self.log.error('Unable to convert CADD version {} to float.'.format(version_build))
                            raise ParserError(
                                "Could not convert header GRCh build (type = {}) to float.".format(
                                    type(version_build)))

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
