from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.exporter import Exporter
from src.main.python.core.config_reader import ConfigReader
from src.main.python.resources.parsers.input_parser import InputParser
from src.main.python.resources.parsers.input_header_parser import \
    InputHeaderParser
from src.main.python.resources.checkers.input_version_checker import \
    InputVersionChecker
from src.main.python.resources.imputers.capice_imputing import CapiceImputing
from src.main.python.resources.preprocessors.preprocessor import PreProcessor
from src.main.python.resources.annotaters.annotator import Annotator
from src.main.python.core.input_checker import InputChecker
from src.main.python.resources.preprocessors.load_file_postprocessor import \
    LoadFilePostProcessor


class Main:
    """
    Main class of CAPICE to call the different modules to impute,
    preprocess and eventually predict a score over a CAPICE annotated file.
    """
    def __init__(self,
                 __program__, __author__, __version__,
                 input_loc, output_loc):

        # Order is important here
        self.manager = CapiceManager()
        self.log = Logger().logger

        # Config loading
        self.config = ConfigReader()

        # Welcome message

        self.log.info(
            'Thank you for using {}, version: {}, created by: {}.'.format(
                __program__,
                __version__,
                __author__
            )
        )

        # Order is less important here

        self.log.info('Arguments passed. Starting program.')
        self.infile = input_loc
        self.log.debug(
            'Input argument -i / --input confirmed: {}'.format(self.infile)
        )
        self.output = output_loc
        self.log.debug(
            'Output directory -o / --output confirmed: {}'.format(self.output)
        )
        config_vep_version = self.config.get_default_value('vepversion')
        self.log.debug(
            'Config VEP version confirmed: {}'.format(
                config_vep_version
            )
        )
        config_genome_build = self.config.get_default_value('genomebuild')
        self.log.debug(
            'Config Genome build confirmed: {}'.format(
                config_genome_build
            )
        )
        self.log.debug('Force flag confirmed: {}'.format(self.manager.force))

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        capice_data = self.load_file()
        capice_data = self.annotate(loaded_data=capice_data)
        capice_data = self.impute(loaded_data=capice_data)
        preprocessing_instance, capice_data = self.preprocess(
            loaded_data=capice_data,
            train=False
        )
        capice_data = self.predict(
            loaded_data=capice_data,
            preprocessing_instance=preprocessing_instance
        )
        self._export(datafile=capice_data)

    def load_file(self):
        """
        Function to load the input file into main
        :return: pandas DataFrame
        """
        is_gzipped = False
        if self.infile.endswith('.gz'):
            is_gzipped = True
        input_header_parser = InputHeaderParser(
            is_gzipped=is_gzipped,
            input_file_loc=self.infile
        )
        skip_rows = input_header_parser.get_skip_rows()
        # InputChecker().check_reference(
        #     reference=self.manager.reference_genome
        # )
        file_vep_version = input_header_parser.get_vep_version()
        file_grch_build = input_header_parser.get_grch_build()
        InputVersionChecker(
            config_vep_version=self.manager.config_vep_version,
            file_vep_version=file_vep_version,
            config_grch_build=self.manager.config_grch_build,
            file_grch_build=file_grch_build
        )
        input_parser = InputParser()
        input_file = input_parser.parse(
            input_file_loc=self.infile,
            skip_rows=skip_rows
        )
        post_load_processor = LoadFilePostProcessor(dataset=input_file)
        input_file = post_load_processor.process()
        return input_file

    @staticmethod
    def annotate(loaded_data):
        """
        Function to annotate the VEP file to a CAPICE file
        """
        annotator = Annotator(dataset=loaded_data)
        annotated_data = annotator.annotate()
        return annotated_data

    @staticmethod
    def impute(loaded_data, train=False):
        """
        Function to perform imputing and converting of categorical features
        """
        capice_imputer = CapiceImputing(train=train)
        capice_data = capice_imputer.impute(loaded_data)
        return capice_data

    @staticmethod
    def preprocess(loaded_data, train: bool):
        """
        Function to perform the preprocessing of a datafile to be ready for
        CAPICE imputing.
        :param loaded_data: Pandas dataframe of the imputed CAPICE data
        :param train: bool
        """
        preprocessor = PreProcessor(is_train=train)
        capice_data = preprocessor.preprocess(datafile=loaded_data)
        return preprocessor, capice_data

    @staticmethod
    def predict(loaded_data, preprocessing_instance):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        capice_data = preprocessing_instance.predict(datafile=loaded_data)
        return capice_data

    def _export(self, datafile):
        """
        Function to prepare the data to be exported
        """
        Exporter(file_path=self.output).export_capice_prediction(
            datafile=datafile
        )
