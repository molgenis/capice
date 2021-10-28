from abc import ABC, abstractmethod

from src.main.python.core.logger import Logger
from src.main.python.core.exporter import Exporter
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.processors.processor import Processor
from src.main.python.resources.predictors.Predictor import Predictor
from src.main.python.resources.parsers.input_parser import InputParser
from src.main.python.resources.imputers.capice_imputing import CapiceImputing
from src.main.python.resources.preprocessors.preprocessor import PreProcessor
from src.main.python.resources.preprocessors.load_file_postprocessor import \
    LoadFilePostProcessor
from src.main.python.resources.validators import PostFileParseValidator


class Main(ABC):
    """
    Main class of CAPICE that contains methods to help the different modes to
    function.
    """
    def __init__(self, input_loc, output_loc):
        # Assumes CapiceManager has been initialized & filled.
        self.manager = CapiceManager()
        self.log = Logger().logger

        self.log.info('Initiating selected mode.')

        # Input file.
        self.infile = input_loc
        self.log.debug('Input argument -i / --input confirmed: %s',
                       self.infile)

        # Output file.
        self.output = output_loc
        self.log.debug(
            'Output directory -o / --output confirmed: %s', self.output
        )

    @abstractmethod
    def run(self):
        pass

    def _load_file(self, additional_required_features=()):
        """
        Function to load the input TSV file into main
        :return: pandas DataFrame
        """
        input_parser = InputParser()
        input_file = input_parser.parse(
            input_file_loc=self.infile
        )
        post_load_processor = LoadFilePostProcessor(dataset=input_file)
        input_file = post_load_processor.process()
        validator = PostFileParseValidator()
        # Individual calls to the validator for error readability
        validator.validate_chrom_pos(input_file)
        validator.validate_n_columns(input_file)
        validator.validate_minimally_required_columns(
            input_file,
            additional_required_features=additional_required_features
        )
        return input_file

    @staticmethod
    def process(loaded_data):
        """
        Function to process the VEP features to CAPICE features.
        """
        processor = Processor(dataset=loaded_data)
        processed_data = processor.process()
        return processed_data

    @staticmethod
    def impute(loaded_data, impute_values):
        """
        Function to perform imputing over the loaded data.
        self.model can be None, but impute_json has to be defined in that case.
        """
        capice_imputer = CapiceImputing(
            impute_values=impute_values
        )
        capice_data = capice_imputer.impute(loaded_data)
        return capice_data

    @staticmethod
    def preprocess(loaded_data, impute_keys, model_features=None):
        """
        Function to perform the preprocessing of the loaded data to convert
        categorical columns.
        :param loaded_data: Pandas dataframe of the imputed CAPICE data
        :param impute_keys: list, all the keys of the impute values that could
        potentially contain a "O" dtype within Pandas (string, categorical etc.)
        :param model_features: list (default None), a list containing all
        the features present within a model file. When set to None,
        PreProcessor will activate the train protocol.
        """
        preprocessor = PreProcessor(
            impute_keys=impute_keys,
            model_features=model_features
        )
        capice_data = preprocessor.preprocess(loaded_data)
        return capice_data

    @staticmethod
    def _export(dataset, output):
        """
        Function to prepare the data to be exported
        """
        Exporter(file_path=output).export_capice_prediction(
            datafile=dataset
        )
