#!/usr/bin/env python3

from src.utilities.utilities import convert_cla_to_str, convert_cla_to_float, convert_cla_to_full_string
from src.command_line_supporter import ArgumentSupporter
from src.global_manager import CapiceManager
from src.errors.errors import InputError
from src.input_checker import LogChecker, InputChecker
from src.main_train import Train

__program__ = 'Training CAPICE models'
__author__ = 'Shuang Li, Robert Sietsma and Molgenis'
__license__ = 'LGPL-3.0'
__version__ = 1.0
__description__ = "{} (version: {}) is a program developed and maintained by {}. " \
                  "The program facilitates a way to create new CAPICE like models." \
                  "This program is developed under the {} license and is provided 'as-is' without any warranty " \
                  "or indemnification of any kind.".format(__program__, __version__, __author__, __license__)


def main():
    """
    Gathering of all command line arguments and checking the input, output and log location. Setting global variables
    and then calling the main_train.py which will perform the actual calling to the modules required to create a new
    CAPICE like model.
    """
    arguments = ArgumentSupporter(description=__description__, type_cmd='train')
    input_loc = convert_cla_to_str(arguments.get_argument('input'))
    balanced = convert_cla_to_str(arguments.get_argument('balanced_input'))
    output_loc = convert_cla_to_str(arguments.get_argument('output'))
    log_loc = convert_cla_to_str(arguments.get_argument('log_file'))
    overwrite_impute_file = convert_cla_to_full_string(arguments.get_argument('overwrite_impute_file'))
    verbose = arguments.get_argument('verbose')
    default = arguments.get_argument('default')
    force = arguments.get_argument('force')
    disable_logfile = arguments.get_argument('disable_logfile')
    specified_default = convert_cla_to_str(arguments.get_argument('specified_default'))
    split = convert_cla_to_float(arguments.get_argument('split'))
    early_exit = arguments.get_argument('exit')
    train_test_split = convert_cla_to_float(arguments.get_argument('train_test_size'))

    _check_input(input_loc, balanced)

    log_checker = LogChecker(log_loc=log_loc, output_loc=output_loc)
    log_loc = log_checker.check_log_loc()

    input_checker = InputChecker()
    input_checker.check_output_loc(output_loc=output_loc)

    manager = CapiceManager()
    manager.set_now()
    manager.set_log_loc(log_loc=log_loc)
    manager.set_verbose(verbose=verbose)
    manager.set_force(force=force)
    manager.disable_logfile(disable_logfile=disable_logfile)
    manager.set_overwrite_impute(overwrite_impute=overwrite_impute_file)

    train = Train(__program__=__program__,
                  __author__=__author__,
                  __version__=__version__,
                  input_loc=input_loc,
                  output_loc=output_loc,
                  balanced_loc=balanced,
                  default=default,
                  specified_default=specified_default,
                  split=split,
                  early_exit=early_exit,
                  train_test_size=train_test_split)

    train.main()


def _check_input(data_loc, balanced_loc):
    """
    Function to check if either data_loc or balanced_loc is given
    :param data_loc: path-like
    :param balanced_loc: path-like
    """
    if data_loc is None and balanced_loc is None:
        raise InputError('Data location must be specified.')


if __name__ == '__main__':
    main()
