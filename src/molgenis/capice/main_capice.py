import typing
from abc import ABC, abstractmethod

import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.enums import Column
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.input_parser import InputParser
from molgenis.capice.core.capice_exporter import CapiceExporter
from molgenis.capice.utilities.preprocessor import PreProcessor
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

    def preprocess(self, loaded_data, input_features: list, train: bool = False):
        """
        Function to perform the preprocessing of the loaded data to convert
        categorical columns.
        :param loaded_data: Pandas dataframe of the imputed CAPICE data
        :param input_features: list, a list containing either all the features present within a
        model file (in case train=False) or a list containing all the features that the user
        supplied in the train_features.json (in case train=True).
        :param train: bool, whenever the train protocol should be started or not.

        Note: please adjust self.exclude_features: to include all of the
        features that the preprocessor should NOT process.
        Features chr_pos_ref_alt, chr and pos are hardcoded and
        thus do not have to be included.
        """
        preprocessor = PreProcessor(
            exclude_features=self.exclude_features,
            input_features=input_features,
            train=train
        )
        capice_data = preprocessor.preprocess(loaded_data)
        return capice_data

    def _export(self, dataset, output):
        """
        Function to prepare the data to be exported
        """
        CapiceExporter(file_path=output, output_given=self.output_given).export_capice_prediction(
            datafile=dataset)
