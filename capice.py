from src.command_line_supporter import ArgumentSupporter
from src.input_checker import InputChecker
from src.utilities.utilities import convert_cla_to_str, convert_cla_to_int,\
    convert_cla_to_float
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
    model_loc = convert_cla_to_str(cla.get_argument('model'))
    log_loc = convert_cla_to_str(cla.get_argument('log_file'))
    genome_build = convert_cla_to_int(cla.get_argument('genome_build'))
    cadd_build = convert_cla_to_float(cla.get_argument('cadd_build'))
    verbose = cla.get_argument('verbose')

    # Checking the inputs.

    input_checker = InputChecker(output_loc=output_loc,
                                 log_loc=log_loc)

    input_checker.check_cadd_header(input_loc, cadd_build, genome_build)

    capice_main = Main(input_loc=input_loc,
                       output_loc=output_loc,
                       log_loc=log_loc,
                       genome_build=genome_build,
                       cadd_build=cadd_build,
                       verbose=verbose)
    capice_main.run()


if __name__ == '__main__':
    main()
