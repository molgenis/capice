#!/usr/bin/env python3

from src.main.python.resources.utilities.utilities import convert_cla_to_str, convert_cla_to_float, convert_cla_to_full_string
from src.main.python.core.command_line_supporter import ArgumentParser
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.input_checker import LogChecker, InputChecker
from src.main_train import Train
from datetime import datetime

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
    arguments = ArgumentParser(description=__description__, type_cmd='train')
    input_loc = convert_cla_to_str(arguments.get_argument('input'))
    balance = arguments.get_argument('balance')
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

    log_checker = LogChecker(log_loc=log_loc, output_loc=output_loc)
    log_loc = log_checker.check_log_loc()

    input_checker = InputChecker()
    input_checker.check_output_loc(output_loc=output_loc)

    manager = CapiceManager()
    manager.now = datetime.now()
    manager.log_loc = log_loc
    manager.verbose = verbose
    manager.force = force
    manager.disable_logfile = disable_logfile
    manager.overwrite_impute = overwrite_impute_file

    train = Train(__program__=__program__,
                  __author__=__author__,
                  __version__=__version__,
                  input_loc=input_loc,
                  output_loc=output_loc,
                  balance=balance,
                  default=default,
                  specified_default=specified_default,
                  split=split,
                  early_exit=early_exit,
                  train_test_size=train_test_split)

    train.main()


if __name__ == '__main__':
    main()
