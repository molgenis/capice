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
from src.main.python.resources.Validators import PostFileParseValidator, \
    PostVEPProcessingValidator


class Main:
    """
    Main class of CAPICE to call the different modules to impute,
    preprocess and eventually predict a score over a CAPICE annotated file.
    """
    def __init__(self, input_loc, model, output_loc):

        # Order is important here
        self.manager = CapiceManager()
        self.log = Logger().logger

        # Order is less important here

        self.log.info('Arguments passed. Starting program.')
        self.infile = input_loc
        self.log.debug('Input argument -i / --input confirmed: %s', self.infile)
        self.model = model
        self.output = output_loc
        self.log.debug(
            'Output directory -o / --output confirmed: %s', self.output
        )
        self.log.debug('Force flag confirmed: %s', self.manager.force)

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        capice_data = self.load_file()
        capice_data = self.process(loaded_data=capice_data)
        capice_data = self.impute(loaded_data=capice_data)
        capice_data = self.preprocess(loaded_data=capice_data, train=False)
        capice_data = self.predict(loaded_data=capice_data)
        self._export(dataset=capice_data)

    def load_file(self, additional_required_features=()):
        """
        Function to load the input file into main
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

    def process(self, loaded_data):
        """
        Function to process the VEP file to a CAPICE file
        """
        processor = Processor(dataset=loaded_data)
        processed_data = processor.process()
        validator = PostVEPProcessingValidator(self.model)
        validator.validate_features_present(processed_data)
        return processed_data

    def impute(self, loaded_data, impute_json=None):
        """
        Function to perform imputing and converting of categorical features
        """
        capice_imputer = CapiceImputing(
            model=self.model,
            impute_json=impute_json
        )
        capice_data = capice_imputer.impute(loaded_data)
        return capice_data

    def preprocess(self, loaded_data, train: bool):
        """
        Function to perform the preprocessing of a datafile to be ready for
        CAPICE imputing.
        :param loaded_data: Pandas dataframe of the imputed CAPICE data
        :param train: bool
        """
        preprocessor = PreProcessor(model=self.model, is_train=train)
        capice_data = preprocessor.preprocess(loaded_data)
        return capice_data

    def predict(self, loaded_data):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        predictor = Predictor(self.model)
        capice_data = predictor.predict(loaded_data)
        return capice_data

    def _export(self, dataset):
        """
        Function to prepare the data to be exported
        """
        Exporter(file_path=self.output).export_capice_prediction(
            datafile=dataset
        )
