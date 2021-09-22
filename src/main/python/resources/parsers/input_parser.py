import logging
logger = logging.getLogger(__name__)
import pandas as pd


class InputParser:
    def __init__(self):
        self.sep = '\t'

    def set_separator(self, sep: str):
        """
        Function to overwrite the default separator 'tab'.
        Currently has no real function, but might be implemented
        in the future if the default separator in the VEP output changes and
        the separator has to be dynamically changed.

        :param sep: str, to be used separator in the pandas.read_csv call
        """
        self.sep = sep

    def parse(self, input_file_loc: str, skip_rows: int):
        """
        Class to start the parsing of additional information from the input
        file.

        :param input_file_loc: str, direction to the input file
        :param skip_rows: int,
            the amount of comment strings pandas has to skip first
        """
        if self.sep == '\t':
            used_sep = 'Tab'
        else:
            used_sep = self.sep
        logger.info(
            'Reading VEP file from: %s using separator: %s',
                input_file_loc,
                used_sep
            )
        input_file = pd.read_csv(
            input_file_loc,
            sep=self.sep,
            skiprows=skip_rows,
            na_values='.',
            low_memory=False
        )
        input_file.dropna(how='all', inplace=True)
        input_file.drop_duplicates(inplace=True)
        logger.info('Input file at %s loaded with %s samples.',
            input_file_loc,
            input_file.shape[0]
        )
        return input_file
