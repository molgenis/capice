import typing
from abc import ABC, abstractmethod

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import Column
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.input_parser import InputParser
from molgenis.capice.core.capice_exporter import CapiceExporter
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

    def _load_file(self, additional_required_features: list = None):
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
    @abstractmethod
    def process(loaded_data, process_features: typing.Collection):
        pass

    @staticmethod
    def categorical_process(loaded_data,
                            processing_features: dict | None = None,
                            train_features: list | None = None):
        processor = CategoricalProcessor()
        capice_data, processed_features = processor.process(
            loaded_data,
            processable_features=train_features,
            predetermined_features=processing_features
        )
        return capice_data, processed_features

    def _export(self, dataset, output):
        """
        Function to prepare the data to be exported
        """
        CapiceExporter(file_path=output, output_given=self.output_given).export_capice_prediction(
            datafile=dataset)
