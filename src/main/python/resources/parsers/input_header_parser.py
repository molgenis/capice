import logging
logger = logging.getLogger(__name__)
from src.main.python.core.global_manager import CapiceManager
import warnings
import gzip


class InputHeaderParser:
    """
    Autonomous class to parse just the header of the input file to get the
    amount of comment lines that pandas should skip when reading.
    """

    def __init__(self, is_gzipped: bool, input_file_loc: str):
        self.manager = CapiceManager()
        logger.info('Starting to parse input file header.')
        self.is_gzipped = is_gzipped
        self.input_file_loc = input_file_loc
        self.header = ''
        self.header_build = False
        self.header_version = False
        self.header_present = False
        self.file_type = None
        self.skip_rows = 0
        self._parse_header()
        if self.header_present:
            logger.info(
                "Input file header successfully identified: %s",self.header.strip()
            )
            self._get_file_type()
        else:
            logger.warning(
                'Unable to parse input file header, header not located. '
                'Does the header start with "##"?'
            )

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
                self._check_vep_version(line=line)
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

    def _check_vep_version(self, line):
        if line.startswith('##VEP="'):
            self._parse_vep_version(line)

    def _parse_vep_version(self, line):
        for annotation in line.split(' '):
            if annotation.startswith('##VEP'):
                self.header_version = float(
                    annotation.split('v')[1].split('"')[0]
                )
                logger.info(
                    'Header VEP version identified: %s', self.header_version
                )
            elif annotation.startswith('assembly'):
                self.header_build = int(annotation.split('h')[1].split('.')[0])
                logger.info(
                    'Header GRCh build identified: %s', self.header_build
                )

    def _get_file_type(self):
        if not self.header.startswith('## VEP VCF to CAPICE tsv converter'):
            warning_message = 'Unable to recognize origin of input file.'
            logger.warning(warning_message)
            warnings.warn(warning_message)

    def get_skip_rows(self):
        """
        Function to return the integer value of how many rows pandas.read_csv()
        should skip to reach the data.

        :return: int
        """
        return self.skip_rows

    def get_vep_version(self):
        """
        Function to return the float value of the VEP version used to generate
        the input file.

        :return: float
        """
        return self.header_version

    def get_grch_build(self):
        """
        Function to return the float value of the GRCh build used to generate
        the input file.

        :return: int
        """
        return self.header_build
