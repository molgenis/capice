import os
from abc import ABC, abstractmethod

import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import Column
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.input_parser import InputParser
from molgenis.capice.core.capice_exporter import CapiceExporter
from molgenis.capice.utilities.manual_vep_processor import ManualVEPProcessor
from molgenis.capice.utilities.categorical_processor import CategoricalProcessor
from molgenis.capice.utilities.load_file_postprocessor import LoadFilePostProcessor
from molgenis.capice.validators.post_file_parse_validator import PostFileParseValidator


class Main(ABC):
    """
    Main class of CAPICE that contains methods to help the different modes to
    function.
    """

    def __init__(self, input_path, output_path, output_given):
        # Assumes CapiceManager has been initialized & filled.
        self.manager = CapiceManager()
        self.log = Logger().logger

        self.log.info('Initiating selected mode.')

        # Input file.
        self.infile = input_path
        self.log.debug('Input argument -i / --input confirmed: %s', self.infile)

        # Output file.
        self.output = output_path
        self.log.debug('Output directory -o / --output confirmed: %s', self.output)
        self.output_given = output_given

        # Preprocessor global exclusion features
        # Overwrite in specific module if features are incorrect
        self.exclude_features = [Column.gene_name.value,
                                 Column.gene_id.value,
                                 Column.id_source.value,
                                 Column.feature.value,
                                 Column.feature_type.value]

    @abstractmethod
    def run(self):
        pass

    def _load_file(self, additional_required_features: list | None = None):
        """
        Function to load the input TSV file into main
        :return: pandas DataFrame
        """
        input_parser = InputParser()
        input_file = input_parser.parse(input_file_path=self.infile)
        post_load_processor = LoadFilePostProcessor(dataset=input_file)
        input_file = post_load_processor.process()
        validator = PostFileParseValidator()
        # Individual calls to the validator for error readability
        validator.validate_variants_present(input_file)
        validator.validate_chrom_pos(input_file)
        validator.validate_n_columns(input_file)
        validator.validate_minimally_required_columns(
            input_file,
            additional_required_features=additional_required_features
        )
        return input_file

    @staticmethod
    def process(loaded_data: pd.DataFrame, process_features: list[str]) -> tuple[
        pd.DataFrame, dict[str, list[str]]
    ]:
        # Returns might look funky, but Google pydoc does not support multiple return statements.
        """
        Function to call the ManualVEPProcessor over loaded_data using the supplied
        process_features list.

        Args:
            loaded_data:
                The pandas dataframe over which the VEP features should be processed.

            process_features:
                List containing either all input features, possibly containing VEP features (in
                the case of train) or already all input features that can be VEP processed (in
                case of predict).

        Returns:
            tuple:
                Tuple [0] containing: The output dataframe containing all VEP processed features
                according to process_features. Depending on the property "drop" will drop the
                feature present in process_features from the columns of the output dataframe.
                Tuple [1] containing: The output dictionary containing the VEP feature (key)
                and the derivative features that originate from said VEP feature (value).
                The property "drop" is of no influence here.
        """
        processor = ManualVEPProcessor()
        processed_data = processor.process(loaded_data, process_features)
        processed_features = processor.get_feature_processes()
        # No validation, since that is specific to predict.
        # Also predict doesn't technically need processed_features, but within predict the first
        # argument in the tuple can just be indexed.
        # Still returning both is relevant, in case we want to validate the processed_features in
        # the future for predict.
        return processed_data, processed_features

    @staticmethod
    def categorical_process(loaded_data: pd.DataFrame,
                            processing_features: dict[str, list[str]] | None = None,
                            train_features: list | None = None):
        processor = CategoricalProcessor()
        capice_data, processed_features = processor.process(
            loaded_data,
            processable_features=train_features,
            predetermined_features=processing_features
        )
        return capice_data, processed_features

    def _export(self, dataset: pd.DataFrame, output: os.PathLike):
        """
        Function to prepare the data to be exported
        """
        CapiceExporter(file_path=output, output_given=self.output_given).export_capice_prediction(
            datafile=dataset)
