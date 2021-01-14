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
        used_sep = ""
        if self.sep == '\t':
            used_sep = 'Tab'
        else:
            used_sep = self.sep
        self.log.info(
            'Reading CADD file from: {} using separator: {}'.format(
                cadd_file_loc,
                used_sep
            ))
        if header_present:
            header = 1
        else:
            header = 0
        cadd_file = pd.read_csv(cadd_file_loc, sep=self.sep, header=header, na_values='.', low_memory=False)
        cadd_file.dropna(how='all', inplace=True)
        cadd_file.drop_duplicates(inplace=True)
        self.log.info('CADD file at {} loaded with {} samples.'.format(
            cadd_file_loc,
            cadd_file.shape[0]
        ))
        return cadd_file
