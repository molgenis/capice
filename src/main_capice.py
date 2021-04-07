from src.main.python.core.logger import Logger
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.exporter import Exporter
from src.main.python.resources.parsers.cadd_parser import CaddParser
from src.main.python.resources.parsers.cadd_header_parser import CaddHeaderParser
from src.main.python.resources.imputers.cadd_imputing import CaddImputing
from src.main.python.resources.checkers.cadd_version_checker import CaddVersionChecker
from src.main.python.resources.preprocessors.preprocessor import PreProcessor


class Main:
    """
    Main class of CAPICE to call the different modules to impute, preprocess and eventually predict a score over a CADD
    annotated file.
    """
    def __init__(self,
                 __program__, __author__, __version__,
                 input_loc, output_loc,
                 genome_build, cadd_build):

        # Order is important here
        self.manager = CapiceManager()
        self.log = Logger().logger

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
        self.cla_genome_build = genome_build
        self.log.debug('Genome build -gb / --genome_build confirmed: {}'.format(self.cla_genome_build))
        self.cla_cadd_version = cadd_build
        self.log.debug('CADD build -cb / --cadd_build confirmed: {}'.format(self.cla_cadd_version))
        self.log.debug('Force flag confirmed: {}'.format(self.manager.force))

    def run(self, train: bool):
        """
        Function to make CAPICE run in a prediction matter.
        """
        cadd_data = self.load_file()
        cadd_data = self.impute(loaded_cadd_data=cadd_data)
        preprocessing_instance, cadd_data = self.preprocess(loaded_cadd_data=cadd_data, train=train)
        if not train:
            cadd_data = self.predict(loaded_cadd_data=cadd_data, preprocessing_instance=preprocessing_instance)
            self._export(datafile=cadd_data)
        else:
            return cadd_data

    def load_file(self):
        """
        Function to load the CADD file into main
        :return: pandas DataFrame
        """
        is_gzipped = False
        if self.infile.endswith('.gz'):
            is_gzipped = True
        cadd_header_parser = CaddHeaderParser(
            is_gzipped=is_gzipped,
            cadd_file_loc=self.infile
        )
        header_present = cadd_header_parser.get_header_present()
        header_version = cadd_header_parser.get_header_version()
        header_build = cadd_header_parser.get_header_build()
        CaddVersionChecker(
            cla_cadd_version=self.cla_cadd_version,
            cla_grch_build=self.cla_genome_build,
            file_cadd_version=header_version,
            file_grch_build=header_build
        )
        cadd_parser = CaddParser()
        cadd_file = cadd_parser.parse(
            cadd_file_loc=self.infile,
            header_present=header_present
        )
        return cadd_file

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
