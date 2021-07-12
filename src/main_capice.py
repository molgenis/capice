from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.exporter import Exporter
from src.main.python.core.config_reader import ConfigReader
from src.main.python.resources.parsers.input_parser import InputParser
from src.main.python.resources.parsers.input_header_parser import InputHeaderParser
from src.main.python.resources.imputers.cadd_imputing import CaddImputing
from src.main.python.resources.checkers.cadd_version_checker import CaddVersionChecker
from src.main.python.resources.preprocessors.preprocessor import PreProcessor
from src.main.python.resources.annotaters.annotator import Annotator
from src.main.python.resources.enums.sections import FileType
from src.main.python.core.input_checker import InputChecker
from src.main.python.resources.preprocessors.load_file_preprocessor import LoadFilePreProcessor


class Main:
    """
    Main class of CAPICE to call the different modules to impute, preprocess and eventually predict a score over a CADD
    annotated file.
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

        self.log.info('Thank you for using {}, version: {}, created by: {}.'.format(
            __program__,
            __version__,
            __author__
        ))

        self.log.info('Verbose -v / --verbose confirmed: {}'.format(self.manager.verbose))

        # Order is less important here

        self.log.info('Arguments passed. Starting program.')
        self.infile = input_loc
        self.log.debug('Input argument -i / --input confirmed: {}'.format(self.infile))
        self.output = output_loc
        self.log.debug('Output directory -o / --output confirmed: {}'.format(self.output))
        self.cla_genome_build = self.config.get_default_value('genomebuild')
        self.log.debug('Genome build -gb / --genome_build confirmed: {}'.format(self.cla_genome_build))
        self.cla_cadd_version = self.config.get_default_value('caddversion')
        self.log.debug('CADD build -cb / --cadd_build confirmed: {}'.format(self.cla_cadd_version))
        self.log.debug('Force flag confirmed: {}'.format(self.manager.force))
        self.file_type = None

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        cadd_data = self.load_file()
        if self.file_type == FileType.VEP.value:
            cadd_data = self.annotate(loaded_data=cadd_data)
        cadd_data = self.impute(loaded_cadd_data=cadd_data)
        preprocessing_instance, cadd_data = self.preprocess(loaded_cadd_data=cadd_data, train=False)
        cadd_data = self.predict(loaded_cadd_data=cadd_data, preprocessing_instance=preprocessing_instance)
        self._export(datafile=cadd_data)

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
        self.file_type = input_header_parser.get_file_type()
        skip_rows = input_header_parser.get_skip_rows()
        if self.file_type == FileType.CADD.value:
            header_version = input_header_parser.get_header_version()
            header_build = input_header_parser.get_header_build()
            CaddVersionChecker(
                cla_cadd_version=self.cla_cadd_version,
                cla_grch_build=self.cla_genome_build,
                file_cadd_version=header_version,
                file_grch_build=header_build
            )
        else:
            InputChecker().check_cadd_db_and_reference(
                cadd_snvs_db=self.manager.cadd_snvs_database,
                cadd_indels_db=self.manager.cadd_indels_database,
                reference=self.manager.reference_genome
            )
        input_parser = InputParser()
        input_file = input_parser.parse(
            input_file_loc=self.infile,
            skip_rows=skip_rows
        )
        post_load_processor = LoadFilePreProcessor(dataset=input_file)
        input_file = post_load_processor.process()
        return input_file

    @staticmethod
    def annotate(loaded_data):
        """
        Function to annotate the VEP file to a CADD like file
        """
        annotator = Annotator(dataset=loaded_data)
        annotated_data = annotator.annotate()
        return annotated_data

    @staticmethod
    def impute(loaded_cadd_data):
        """
        Function to perform imputing and converting of categorical features
        """
        cadd_imputer = CaddImputing()
        cadd_data = cadd_imputer.impute(loaded_cadd_data)
        return cadd_data

    @staticmethod
    def preprocess(loaded_cadd_data, train: bool):
        """
        Function to perform the preprocessing of a datafile to be ready for CAPICE imputing.
        :param loaded_cadd_data: Pandas dataframe of the imputed CADD data
        :param train: bool
        """
        preprocessor = PreProcessor(is_train=train)
        cadd_data = preprocessor.preprocess(datafile=loaded_cadd_data)
        return preprocessor, cadd_data

    @staticmethod
    def predict(loaded_cadd_data, preprocessing_instance):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        cadd_data = preprocessing_instance.predict(datafile=loaded_cadd_data)
        return cadd_data

    def _export(self, datafile):
        """
        Function to prepare the data to be exported
        """
        Exporter(file_path=self.output).export_capice_prediction(datafile=datafile)
