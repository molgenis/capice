#!/usr/bin/env python3

"""
CAPICE.py is a module of CAPICE that is supposed to be called when the user wants to make a prediction over a CADD
annotated file. It's use is to gather all Command Line Arguments, check some, provide the global manager
(./src/global_manager.py CapiceManager) with arguments that are used in multiple modules and provide
./src/main_capice.py with it's wanted arguments.
"""

from src.main.python.core.command_line_supporter import ArgumentParser
from src.main.python.core.input_checker import InputChecker, LogChecker
from src.main.python.resources.utilities.utilities import convert_cla_to_str
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.config_reader import ConfigReader
from src.main_capice import Main
from src.main_train import Train
from datetime import datetime

__program__ = 'CAPICE'
__author__ = 'Shuang Li, Robert Sietsma and Molgenis'
__license__ = 'LGPL-3.0'
__version__ = 2.0
__description__ = "{} (version: {}) is a program developed and maintained by {}. " \
                  "The program facilitates a pathogenicity prediction for a CADD annotated VCF file. " \
                  "This program is developed under the {} license and is provided 'as-is' without any warranty " \
                  "or indemnification of any kind.".format(__program__, __version__, __author__, __license__)


def main():
    """
    Gathering of Command Line Arguments (CLAs), checking the log location,
    setting global variables and providing Main.py with it's wanted arguments.
    Converting the CLAs happens because often the CLA is returned as a list.
    """
    cla = ArgumentParser(description=__description__)

    # Getting all arguments.

    input_loc = convert_cla_to_str(cla.get_argument('input'))
    output_loc = convert_cla_to_str(cla.get_argument('output'))
    verbose = cla.get_argument('verbose')
    force = cla.get_argument('force')
    train = cla.get_argument('train')

    # Getting all config settings.

    config = ConfigReader()
    config.parse()
    log_loc = config.get_default_value(key='logfilelocation')

    # Checking the log arguments

    lc = LogChecker(log_loc=log_loc, output_loc=output_loc)
    log_loc = lc.check_log_loc()

    # Checking the input arguments.

    input_checker = InputChecker()

    input_checker.check_input_loc(input_loc=input_loc)
    input_checker.check_output_loc(output_loc=output_loc)

    # Initializing the manager

    manager = CapiceManager()
    manager.now = datetime.now()
    manager.disable_logfile = config.get_misc_value(key='disablelogfile')
    manager.log_loc = log_loc
    manager.verbose = verbose
    manager.overwrite_impute = config.get_overwrite_value(key='imputefile')
    manager.overwrite_model = config.get_overwrite_value(key='modelfile')
    manager.force = force

    if train:
        capice_main = Train(__program__=__program__,
                            __author__=__author__,
                            __version__=__version__,
                            input_loc=input_loc,
                            output_loc=output_loc)
    else:
        capice_main = Main(__program__=__program__,
                           __author__=__author__,
                           __version__=__version__,
                           input_loc=input_loc,
                           output_loc=output_loc)

    capice_main.run()


if __name__ == '__main__':
    main()
