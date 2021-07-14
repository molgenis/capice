"""
    File:         logger.py
    Created:      2019/10/11
    Last Changed:
    Author(s):    M.Vochteloo and R. J. Sietsma

    Copyright 2019 M. Vochteloo and R. J. Sietsma

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import logging
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.utilities.utilities import check_file_exists
import os
import sys


class Logger:
    """
    Singleton logger class developed by both:
    - Martijn Vochteloo
    - Robert Jarik Sietsma.
    Facilitates the python logging library
    """

    class __Logger:
        def __init__(self):
            self.final_log_loc = None
            self.global_settings = CapiceManager()
            self.log_level = self.set_loglevel()
            self.output_loc = self.global_settings.log_loc
            self.create_logfile = self.global_settings.enable_logfile
            self.logger = None
            if self.logger is None:
                self.load_logger()

        def set_loglevel(self):
            """
            Function to set the log level at where messages are printed or
            logged. For more information, see:
            https://docs.python.org/3/library/logging.html#logging-levels
            :return: logging level
            """
            if not self.global_settings.critical_logging_only:
                if self.global_settings.verbose:
                    return logging.NOTSET
                else:
                    return logging.INFO
            else:
                return logging.CRITICAL

        def load_logger(self):
            """
            Function to set up the logger instance with the correct format and
            filename.

            :return: logger instance
            """
            logger = logging.getLogger('CAPICE')
            logger.setLevel(self.log_level)
            console_handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter("%(asctime)s "
                                          "[%(name)s] "
                                          "[%(filename)s] "
                                          "[%(funcName)s] "
                                          "[%(levelname)-4.4s]  "
                                          "%(message)s")
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            if self.create_logfile:
                now = self.global_settings.now
                out_file_name = 'capice_{}'.format(
                    now.strftime("%H%M%S%f_%d%m%Y")
                )
                out_file = self._create_log_export_name(out_file_name)
                self.final_log_loc = out_file
                file_handler = logging.FileHandler(out_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                print('Log location confirmed: {}'.format(out_file))
            else:
                print('Log file disabled. Using Stdout and Stderr.')
            self.logger = logger

        @property
        def logger(self):
            """
            Property to get the logger instance.

            :return: logging.Logger
            """
            return self._logger

        @logger.setter
        def logger(self, value):
            """
            Setter for the logger instance.

            :param value:
            :return:
            """
            self._logger = value

        def get_log_loc(self):
            """
            Function for external modules to request where the log file is
            saved.
            :return: path-like
            """
            return self.final_log_loc

        def _create_log_export_name(self, out_file_name):
            """
            Function to create an unique logfile name
            :param out_file_name: Filename of the logfile
            :return: full export path
            """
            full_export = os.path.join(self.output_loc, out_file_name + '.log')
            partial_export = os.path.join(self.output_loc, out_file_name)
            export_path = None
            if check_file_exists(full_export):
                log_file_exist = True
                counter = 1
                while log_file_exist:
                    attempted_filename = partial_export + '_{}.log'.format(
                        counter
                    )
                    if not check_file_exists(attempted_filename):
                        log_file_exist = False
                        export_path = attempted_filename
                    counter += 1
            else:
                export_path = full_export
            return export_path

    @property
    def logger(self):
        """
        Property to get the logger instance.

        :return: logging.Logger
        """
        return self._logger

    def get_log_loc(self):
        """
        Function to get the real location where the logfile is stored for this
        instance of CAPICE.
        :return: path-like
        """
        pass

    instance = None

    def __new__(cls):
        """
        Class method to set Logger instance
        :return: instance
        """
        if not Logger.instance:
            Logger.instance = Logger.__Logger()
        return Logger.instance

    def __init__(self):
        """
        __init__ method to set instance to Logger.__Logger()
        """
        if not Logger.instance:
            Logger.instance = Logger.__Logger()

    def __getattr__(self, name):
        """
        Method to return the value of the named attribute of name
        :param name: str
        :return: str
        """
        return getattr(self.instance, name)
