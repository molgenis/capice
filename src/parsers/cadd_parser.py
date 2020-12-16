from src.logger import Logger
import pandas as pd


class CaddParser:
    def __init__(self):
        self.sep = '\t'
        self.log = Logger().get_logger()

    def set_separator(self, sep: str):
        """
        Function to overwrite the default separator 'tab'
        :param sep: str, to be used separator in the pandas.read_csv call
        """
        self.sep = sep

    def parse(self, cadd_file_loc: str, header_present: bool):
        """
        Class to start the parsing of additional information from the CADD file and set the CADD version and GRCh build.
        :param cadd_file_loc: str, direction to the cadd file
        :param header_present: bool, whenever the CADD header is present within the file or not
        """
        self.log.info(
            'Reading CADD file from: {} using separator: {}'.format(
                cadd_file_loc,
                self.sep
            ))
        if header_present:
            header = 1
        else:
            header = 0
        cadd_file = pd.read_csv(cadd_file_loc, sep=self.sep, header=header, na_values='.')
        cadd_file.dropna(how='all')
        self.log.info('CADD file at {} loaded with {} samples.'.format(
            cadd_file_loc,
            cadd_file.shape[0]
        ))
        return cadd_file
