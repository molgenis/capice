from src.errors.errors import ParserError
from src.logger import Logger
import gzip


class CaddHeaderParser:
    """
    Class to parse just the header of the CADD file
    """
    def __init__(self, is_gzipped: bool, cadd_file_loc: str):
        self.is_gzipped = is_gzipped
        self.cadd_file_loc = cadd_file_loc
        self.header = None
        self.header_build = None
        self.header_build = None
        self.header_present = False
        self.log = Logger().get_logger()
        self._parse_header()
        if self.header_present:
            self.log.info("CADD file header identified: {}".format(self.header))
            self._get_header_version_and_grch_build()

    def _parse_header(self):
        if self.is_gzipped:
            with gzip.open(self.cadd_file_loc, mode='rt') as file:
                self.header = file.readline().strip()
                self.header_present = True
        else:
            with open(self.cadd_file_loc) as file:
                self.header = file.readline().strip()
                self.header_present = True

    def _get_header_version_and_grch_build(self):
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
