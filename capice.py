#!/usr/bin/env python3

"""
CAPICE.py is a module of CAPICE that is supposed to be called when the user
wants to make a prediction over a VEP annotated file. It's use is to gather all
Command Line Arguments, check some, provide the global manager
(./src/global_manager.py CapiceManager) with arguments that are used in multiple
modules and provide ./src/main_capice.py with it's wanted arguments.
"""

from src.main.python.core.command_line_parser import ArgumentParser
from src.main.python.core.input_checker import InputChecker
from src.main.python.core.log import setup_logger
from src.main.python.resources.utilities.utilities import convert_cla_to_str
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.config_reader import ConfigReader
from src.main_capice import Main
from src.main_train import Train
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

__program__ = 'CAPICE'
__author__ = 'Shuang Li, Robert Sietsma and Molgenis'
__license__ = 'LGPL-3.0'
__version__ = '2.0.0'
__description__ = """{} (version: {}) is a program developed and maintained by 
{}. The program facilitates a pathogenicity prediction for a VEP annotated VCF 
file. This program is developed under the {} license and is provided 'as-is' 
without any warranty or indemnification of any kind.""".format(
    __program__,
    __version__,
    __author__,
    __license__
)


def main():
    """
    Gathering of Command Line Arguments (CLAs), checking the log location,
    setting global variables and providing Main.py with it's wanted arguments.
    Converting the CLAs happens because often the CLA is returned as a list.
    """
    cla = ArgumentParser(description=__description__)

    if cla.get_argument('debug'):
        level = logging.DEBUG
    elif cla.get_argument('verbose'):
        level = logging.INFO
    else:
        level = logging.WARNING
    setup_logger(level)

    # Getting all arguments.
    input_loc = convert_cla_to_str(cla.get_argument('input'))
    output_loc = convert_cla_to_str(cla.get_argument('output'))
    force = cla.get_argument('force')
    train = cla.get_argument('train')
    config_argument = convert_cla_to_str(cla.get_argument('config'))

    # Initializing manager

    manager = CapiceManager()
    manager.config_loc = config_argument
    manager.force = force

    # Getting all config settings.

    config = ConfigReader()
    config.parse()

    # Checking the input arguments.

    input_checker = InputChecker()

    input_loc = input_checker.check_input_loc(input_loc=input_loc)
    input_checker.check_input_output_directories(input_path=input_loc,
                                                 output_path=output_loc)
    output_loc = input_checker.get_output_directory()
    output_filename = input_checker.get_output_filename()
    input_checker.check_output_loc(output_loc=output_loc)

    # Setting the remaining manager variables.

    manager.overwrite_impute = config.get_overwrite_value(key='imputefile')
    manager.overwrite_model = config.get_overwrite_value(key='modelfile')
    manager.config_vep_version = config.get_default_value(key='vepversion')
    manager.config_grch_build = config.get_default_value(key='genomebuild')
    manager.output_filename = output_filename
    manager.reference_genome = config.get_datafiles_value(key='reference')

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
