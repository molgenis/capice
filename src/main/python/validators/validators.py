import os
import warnings
import pandas as pd
from pathlib import Path
from src.main.python.core.logger import Logger
from src.main.python.utilities.sections import Column


class InputValidator:
    """
    Validator for the CLI arguments
    """

    def __init__(self, parser):
        self.parser = parser

    def validate_input_loc(self, input_loc, extension: tuple):
        """
        Function to validate if there is a file at the input location
        :param input_loc: full path to input file
        :param extension: string of what the input file should end with.
        """
        if not os.path.exists(input_loc):
            self.parser.error("Input file does not exist!")
        if not (input_loc.endswith(extension)):
            self.parser.error(
                'Given input file does not match required extension!'
            )

    def validate_output_loc(self, output_loc):
        """
        Function to validate if the output directory exists and,
        if not, make it.
        :param output_loc: path to output folder
        """
        # If the output directory is not present and
        # the parent directory is also not writeable, throw OSError
        if not os.path.isdir(output_loc) and not os.access(
                Path(output_loc).parent, os.W_OK):
            self.parser.error(
                "New output directory cannot be made in a "
                "read/execute only directory!"
            )
        # If the output directory is present but not writable, throw OSError
        elif os.path.isdir(output_loc) and not os.access(output_loc, os.W_OK):
            self.parser.error(
                "Output directory is not writable!"
            )
        # If the output directory is not yet present,
        # but passed the check that it is in a writable parent directory,
        # only warn
        elif not os.path.isdir(output_loc):
            warnings.warn("Output directory does not exist, creating.")
            os.makedirs(output_loc)

        # No else is required, since the else would be to place the output file
        # in a writeable output directory that is already present.


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
            self,
            dataset,
            additional_required_features: list = None
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
            error_message = 'Detected required columns %s not ' \
                            'present within input dataset!'
            self.log.critical(error_message, ', '.join(columns_not_present))
            raise KeyError(error_message % ', '.join(columns_not_present))

    def validate_chrom_pos(self, dataset):
        """
        Function to check if all values of the columns Chr and Pos are present.
        """
        if dataset[Column.chr.value].isnull().values.any():
            error_message = 'Detected gap in Chromosome column! ' \
                            'Please supply a valid dataset.'
            self.log.critical(error_message)
            raise ValueError(error_message)
        if dataset[Column.pos.value].isnull().values.any():
            error_message = 'Detected gap in Position column! ' \
                            'Please supply a valid dataset.'
            self.log.critical(error_message)
            raise ValueError(error_message)


class PostVEPProcessingValidator:
    def __init__(self, model):
        self.model = model
        self.log = Logger().logger

    def validate_features_present(self, datafile):
        """
        Validator to see if all features within the model impute values are
        presently processed.
        """
        features_not_present = []
        for feature in self.model.impute_values.keys():
            if feature not in datafile.columns:
                features_not_present.append(feature)
        if len(features_not_present) > 0:
            error_message = 'Detected required feature(s) %s not ' \
                            'present within VEP processed input file!'
            self.log.critical(error_message, ', '.join(features_not_present))
            raise KeyError(error_message % ', '.join(features_not_present))
