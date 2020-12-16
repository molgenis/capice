from src.logger import Logger
from src.global_manager import CapiceManager
from src.exporter import Exporter
from src.preprocess import PreProcess
from src.parsers.cadd_parser import CaddParser
from src.parsers.cadd_header_parser import CaddHeaderParser
from src.imputers.cadd_imputing import CaddImputing
from src.checkers.cadd_version_checker import CaddVersionChecker
from capice import __program__, __author__, __version__


class Main:
    def __init__(self, input_loc, output_loc,
                 genome_build, cadd_build, force, verbose):
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

        # Setting the exporter force

        self.exporter = Exporter()
        self.exporter.set_force(self.force)

        # Global main variables

        self.cadd_version = None
        self.grch_build = None
        self.cadd_data = None

    def run(self):
        """
        Function to make CAPICE run
        """
        self._load_file()
        self._impute()
        self._preprocess()
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
        cvc = CaddVersionChecker(
            cla_cadd_version=self.cla_cadd_version,
            cla_grch_build=self.cla_genome_build,
            file_cadd_version=header_version,
            file_grch_build=header_build
        )
        self.cadd_version = cvc.get_cadd_version()
        self.grch_build = cvc.get_grch_build()
        cadd_parser = CaddParser()
        self.cadd_file = cadd_parser.parse(
            cadd_file_loc=self.infile,
            header_present=header_present
        )

    def _impute(self):
        """
        Function to perform imputing and converting of categorical features
        """
        cadd_imputing = CaddImputing(
            cadd_version=self.cadd_version,
            grch_build=self.grch_build
        )
        self.cadd_data = cadd_imputing.impute(self.cadd_data)

    def _preprocess(self, train: bool = False):
        pass

    def _predict(self):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        pass

    def _export(self):
        """
        Function to prepare the data to be exported
        """
        pass
