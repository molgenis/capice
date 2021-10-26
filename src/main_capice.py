from abc import ABC, abstractmethod

from main.python.resources.processors.processor import Processor
from src.main.python.core.logger import Logger
from src.main.python.core.exporter import Exporter
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.parsers.input_parser import InputParser
from src.main.python.resources.imputers.capice_imputing import CapiceImputing
from src.main.python.resources.preprocessors.preprocessor import PreProcessor
from src.main.python.resources.preprocessors.load_file_postprocessor import \
    LoadFilePostProcessor
from src.main.python.resources.Validators import PostFileParseValidator


class Main(ABC):
    """
    Main class of CAPICE that contains methods to help the different modes to
    function.
    """
    def __init__(self):
        # Assumes CapiceManager has been initialized & filled.
        self.manager = CapiceManager()
        self.log = Logger().logger

        self.log.info('Initiating selected mode.')

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def load_file(infile, additional_required_features=()):
        """
        Function to load the input file into main
        :return: pandas DataFrame
        """
        input_parser = InputParser()
        input_file = input_parser.parse(
            input_file_loc=infile
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
        Function to process the VEP file to a CAPICE file
        """
        processor = Processor(dataset=loaded_data)
        processed_data = processor.process()
        return processed_data

    @staticmethod
    def impute(loaded_data, model=None, impute_json=None):
        """
        Function to perform imputing and converting of categorical features
        """
        capice_imputer = CapiceImputing(
            model=model,
            impute_json=impute_json
        )
        capice_data = capice_imputer.impute(loaded_data)
        return capice_data

    @staticmethod
    def preprocess(loaded_data, model=None):
        pass
        """
        Function to perform the preprocessing of a datafile to be ready for
        CAPICE imputing.
        :param loaded_data: Pandas dataframe of the imputed CAPICE data
        :param train: bool
        :param model:
        """
        if model is None:
            preprocessor = PreProcessor(model=model, is_train=True)
        else:
            preprocessor = PreProcessor(model=model, is_train=False)
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
