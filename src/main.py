from src.logger import Logger
from src.global_manager import CapiceManager
from src.exporter import Exporter
from src.parsers.cadd_parser import CaddParser
from src.parsers.cadd_header_parser import CaddHeaderParser
from src.imputers.cadd_imputing import CaddImputing
from src.checkers.cadd_version_checker import CaddVersionChecker
from src.preprocessors.preprocessor import PreProcessor


class Main:
    def __init__(self,
                 __program__, __author__, __version__,
                 input_loc, output_loc,
                 genome_build, cadd_build,
                 force, verbose):
        # Order is important here
        self.manager = CapiceManager()
        self.log = Logger().get_logger()
        print('Log location confirmed: {}'.format(Logger().get_log_loc()))
        # Welcome message

        self.log.info('Thank you for using {}, version: {}, created by: {}.'.format(
            __program__,
            __version__,
            __author__
        ))

        self.verbose = verbose
        self.log.info('Verbose -v / --verbose confirmed: '
                      '{}'.format(self.verbose))

        # Order is less important here

        self.log.info('Arguments passed. Starting program.')
        self.infile = input_loc
        self.log.info('Input argument -i / --input confirmed: '
                      '{}'.format(self.infile))
        self.output = output_loc
        self.log.info('Output directory -o / --output confirmed: '
                      '{}'.format(self.output))
        self.cla_genome_build = genome_build
        self.log.info('Genome build -gb / --genome_build confirmed: '
                      '{}'.format(self.cla_genome_build))
        self.cla_cadd_version = cadd_build
        self.log.info('CADD build -cb / --cadd_build confirmed: '
                      '{}'.format(self.cla_cadd_version))
        self.force = force
        self.log.info('Force flag confirmed: '
                      '{}'.format(self.force))

    def run(self):
        """
        Function to make CAPICE run
        """
        cadd_data = self._load_file()
        cadd_data = self._impute(loaded_cadd_data=cadd_data)
        cadd_data, model_instance = self._preprocess(loaded_cadd_data=cadd_data)
        cadd_data = self._predict(preprocessing_instance=model_instance,
                                  loaded_cadd_data=cadd_data)
        pass

    def _load_file(self):
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
    def _impute(loaded_cadd_data):
        """
        Function to perform imputing and converting of categorical features
        """
        cadd_data = CaddImputing().impute(loaded_cadd_data)
        return cadd_data

    @staticmethod
    def _preprocess(loaded_cadd_data, train: bool = False):
        """
        Function to perform the preprocessing of a datafile to be ready for CAPICE imputing.
        :param train: bool
        """
        preprocessor = PreProcessor(is_train=train)
        cadd_data = preprocessor.preprocess(datafile=loaded_cadd_data)
        if not train:
            return cadd_data, preprocessor
        else:
            return cadd_data

    @staticmethod
    def _predict(preprocessing_instance, loaded_cadd_data):
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
        Exporter(file_path=self.output).export(datafile=datafile)
