import pandas as pd

from src.main.python.core.logger import Logger
from src.main.python.utilities.enums import Column


class PostFileParseValidator:
    def __init__(self):
        self.log = Logger().logger

    def validate_n_columns(self, dataset):
        """
        Validator to make sure that at least 4 columns are loaded
        (chr, pos, ref, alt). Does NOT check for the names of these columns!
        """
        if isinstance(dataset, pd.Series) or not dataset.shape[1] >= 4:
            error_message = 'Loaded dataset does NOT have enough features! ' \
                            'Is there a header present that does not start ' \
                            'with ##?'
            self.log.critical(error_message)
            raise KeyError(error_message)

    def validate_minimally_required_columns(
            self, dataset, additional_required_features: list = None
    ):
        """
        Validator for both predict and train to check if the very least columns
        are present (chr, pos, ref, alt) and additionally the additional
        required columns.
        """
        required_columns = [
            Column.chr.value,
            Column.pos.value,
            Column.ref.value,
            Column.alt.value,
        ]
        if additional_required_features is not None:
            for feature in additional_required_features:
                if feature not in required_columns:
                    required_columns.append(feature)
        columns_not_present = []
        for col in required_columns:
            if col not in dataset.columns:
                columns_not_present.append(col)
        if len(columns_not_present) > 0:
            error_message = 'Detected required columns %s not present within input dataset!'
            self.log.critical(error_message, ', '.join(columns_not_present))
            raise KeyError(error_message % ', '.join(columns_not_present))

    def validate_chrom_pos(self, dataset):
        """
        Function to check if all values of the columns Chr and Pos are present.
        """
        if dataset[Column.chr.value].isnull().values.any():
            error_message = 'Detected gap in Chromosome column! Please supply a valid dataset.'
            self.log.critical(error_message)
            raise ValueError(error_message)
        if dataset[Column.pos.value].isnull().values.any():
            error_message = 'Detected gap in Position column! Please supply a valid dataset.'
            self.log.critical(error_message)
            raise ValueError(error_message)
