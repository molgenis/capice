import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import InputColumn
from molgenis.capice.validators.post_file_parse_validator import PostFileParseValidator


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

    def parse(self, input_file_path: str,
              additional_columns: dict[str, str] = {}):
        """
        Class to start the parsing of additional information from the input
        file.

        Args:
            input_file_path: direction to the input file
            additional_columns: additional columns which should be used besides the minimal
            required columns that are always required. The key should be the column name and the
            value its panda's dtype.
        """
        if self.sep == '\t':
            used_sep = 'Tab'
        else:
            used_sep = self.sep
        self.log.info('Reading VEP file from: %s using separator: %s', input_file_path, used_sep)
        min_req_cols = {x.col_input_name for x in PostFileParseValidator.MINIMUM_REQUIRED_COLUMNS}
        input_file = pd.read_csv(input_file_path, sep=self.sep, na_values='.',
                                 usecols=min_req_cols.union({*additional_columns}),
                                 dtype=InputColumn.get_input_name_dtype_dict() | additional_columns)
        message = 'Input file at %s loaded with %s samples.'
        self.log.info(message, input_file_path, input_file.shape[0])
        return input_file
