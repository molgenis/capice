import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import Column
from molgenis.capice.utilities.column_utils import ColumnUtils


class PostFileParseValidator:
    def __init__(self):
        self.log = Logger().logger

    def validate_n_columns(self, dataset):
        """
        Validator to make sure that at least 4 columns are loaded
        (chr, pos, ref, alt). Does NOT check for the names of these columns!
        """
        if isinstance(dataset, pd.Series) or dataset.shape[1] < 4:
            error_message = 'Loaded dataset does NOT have enough features! ' \
                            'Is there a header present that does not start ' \
                            'with ##?'
            self.log.critical(error_message)
            raise KeyError(error_message)

    def validate_variants_present(self, dataset):
        """
        Validator to make sure that there is at least one variant present.
        """
        if dataset.shape[0] == 0:
            error_message = 'Loaded dataset does not contain variants!'
            self.log.critical(error_message)
            raise ValueError(error_message)

    def validate_minimally_required_columns(
            self, dataset, additional_required_features: list | None = None
    ):
        """
        Validator for both predict and train to check if the very least columns
        are present (chr, pos, ref, alt) and additionally the additional
        required columns.
        """
        column_utils = ColumnUtils()
        column_utils.set_specified_columns([
            Column.chr.value,
            Column.pos.value,
            Column.ref.value,
            Column.alt.value,
        ])
        if additional_required_features is not None:
            column_utils.add_to_specified_columns(additional_required_features)
        columns_not_present = column_utils.get_missing_diff_with(dataset.columns)
        if len(columns_not_present) > 0:
            error_message = 'Detected required column %s not present within input dataset!'
            if len(columns_not_present) > 1:
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
