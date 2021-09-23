from src.main.python.core.logger import Logger
import pandas as pd


class InputParser:
    def __init__(self):
        self.log = Logger().logger
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
        self.log.info(
            f'Reading VEP file from: {input_file_loc} '
            f'using separator: {used_sep}'
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
        self.log.info(
            f'Input file at {input_file_loc} loaded with '
            f'{input_file.shape[0]} samples.'
        )
        return input_file
