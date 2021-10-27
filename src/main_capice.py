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
from src.main.python.resources.validators import PostFileParseValidator, \
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

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        capice_data = self.load_file()
        capice_data = self.process(loaded_data=capice_data)
        capice_data = self.impute(
            loaded_data=capice_data,
            impute_values=self.model.impute_values
        )
        capice_data = self.preprocess(loaded_data=capice_data, model=self.model)
        capice_data = self.predict(loaded_data=capice_data)
        self._export(dataset=capice_data)

    def load_file(self, additional_required_features=()):
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

    def process(self, loaded_data):
        """
        Function to process the VEP features to CAPICE features.
        """
        processor = Processor(dataset=loaded_data)
        processed_data = processor.process()
        validator = PostVEPProcessingValidator(self.model)
        validator.validate_features_present(processed_data)
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
    def preprocess(loaded_data, model=None):
        """
        Function to perform the preprocessing of the loaded data to convert
        categorical columns.
        :param loaded_data: Pandas dataframe of the imputed CAPICE data
        :param model: None or XGBClassifier, None for training or loaded custom
        XGBClassifier instance.
        """
        preprocessor = PreProcessor(model=model)
        capice_data = preprocessor.preprocess(loaded_data)
        return capice_data

    def predict(self, loaded_data):
        """
        Function to call model to predict CAPICE scores
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
