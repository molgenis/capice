from src.command_line_supporter import ArgumentSupporter
from src.input_checker import InputChecker, LogChecker
from src.utilities.utilities import convert_cla_to_str, convert_cla_to_int,\
    convert_cla_to_float
from src.global_manager import CapiceManager
from src.main import Main

__program__ = 'CAPICE'
__author__ = 'Shuang Li, Robert Sietsma and Molgenis'
__license__ = 'unknown'
__version__ = 2.0


def main():
    cla = ArgumentSupporter()

    # Getting all arguments.

    input_loc = convert_cla_to_str(cla.get_argument('input'))
    output_loc = convert_cla_to_str(cla.get_argument('output'))
    log_loc = convert_cla_to_str(cla.get_argument('log_file'))
    genome_build = convert_cla_to_int(cla.get_argument('genome_build'))
    cadd_build = convert_cla_to_float(cla.get_argument('cadd_build'))
    verbose = cla.get_argument('verbose')
    force = cla.get_argument('force')

    # Checking the log arguments

    lc = LogChecker(log_loc=log_loc, output_loc=output_loc, verbose=verbose)
    log_loc = lc.check_log_loc()

    # Initializing the manager

    manager = CapiceManager()
    manager.set_force(force=force)
    manager.set_log_loc(log_loc=log_loc)
    manager.set_verbose(verbose)

    # Checking the input arguments.

    input_checker = InputChecker()

    input_checker.check_arguments(input_loc=input_loc, output_loc=output_loc)

    capice_main = Main(input_loc=input_loc,
                       output_loc=output_loc,
                       genome_build=genome_build,
                       cadd_build=cadd_build,
                       force=force,
                       verbose=verbose)
    capice_main.run()


if __name__ == '__main__':
    main()
