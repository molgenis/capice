from src.logger import Logger
from src.global_manager import CapiceManager


class Main:
    def __init__(self, input_loc, output_loc, model_loc, log_loc,
                 genome_build, cadd_build, verbose):
        self.manager = CapiceManager()
        self.manager.set_verbose(verbose)
        self.manager.set_log_loc(log_loc)
        self.log = Logger().get_logger()
        self.verbose = verbose
        self.log.info('Verbose -v / --verbose confirmed: '
                      '{}'.format(self.verbose))
        self.log.info('Arguments passed. Starting program.')
        self.infile = input_loc
        self.log.info('Input argument -i / --input confirmed: '
                      '{}'.format(self.infile))
        self.output = output_loc
        self.log.info('Output directory -o / --output confirmed: '
                      '{}'.format(self.output))
        self.model_loc = model_loc
        self.log.info('Model -m / --model confirmed: '
                      '{}'.format(self.model_loc))
        self.genome_build = genome_build
        self.log.info('Genome build -gb / --genome_build confirmed: '
                      '{}'.format(self.genome_build))
        self.cadd_build = cadd_build
        self.log.info('CADD build -cb / --cadd_build confirmed: '
                      '{}'.format(self.cadd_build))

    def run(self):
        pass
