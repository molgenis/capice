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

import sys
import logging

from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.custom_logging_filter import CustomLoggingFilter


class Logger:
    """
    Singleton logger class developed by both:
    - Martijn Vochteloo
    - Robert Jarik Sietsma.
    Facilitates the python logging library
    """

    class __Logger:
        def __init__(self):
            self.global_settings = CapiceManager()
            self.stdout = False
            self.stdout_filter = []
            self.stderr_loglevel = 50
            self.min_loglevel = 50
            self.set_stderr_loglevel()
            self.logger = None
            if self.logger is None:
                self.load_logger()

        def set_stderr_loglevel(self):
            """
            Function to set the log level at where messages are printed or
            logged. For more information, see:
            https://docs.python.org/3/library/logging.html#logging-levels
            :return: logging level
            """
            if not self.global_settings.critical_logging_only:
                self.stderr_loglevel = 30
                self.min_loglevel = 30
            if self.global_settings.loglevel and self.stderr_loglevel < 50:
                self.stdout = True
                self._set_stdout_filter()

        def _set_stdout_filter(self):
            """
            Required because else Warning, Error and CRITICAL messages are
            printed to sys.stdout.
            """
            logging_info = [logging.INFO]
            logging_debug = logging_info + [logging.DEBUG]
            dict_of_levels = {10: logging_debug, 20: logging_info}
            self.stdout_filter = dict_of_levels[self.global_settings.loglevel]
            self.min_loglevel = self.global_settings.loglevel

        def load_logger(self):
            """
            Function to set up the logger instance with the stdout and stderr
            StreamHandlers (stdout assuming verbose flag is called) and the
            formatter.
            """
            # Making a root logger to make sure the level is set correctly.
            logger = logging.getLogger()
            # Now renaming it to CAPICE.
            logger.name = 'CAPICE'

            # Capture warnings
            logging.captureWarnings(True)

            formatter = logging.Formatter(
                "%(asctime)s "
                "%(levelname)8s: "
                "%(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # Setting the log level to debug, but with an applied filter
            logger.setLevel(self.min_loglevel)

            # sys.stdout (if critical logging only isn't called and one of
            # the verbose flags is called.
            if self.stdout:
                stdout_handler = logging.StreamHandler(sys.stdout)
                stdout_handler.setLevel(self.global_settings.loglevel)
                stdout_handler.setFormatter(formatter)
                # Filter out warning, error and critical messages.
                stdout_handler.addFilter(CustomLoggingFilter(self.stdout_filter))
                logger.addHandler(stdout_handler)

            # sys.stderr
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(self.stderr_loglevel)
            stderr_handler.setFormatter(formatter)
            logger.addHandler(stderr_handler)
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

    @property
    def logger(self):
        """
        Property to get the logger instance.

        :return: logging.Logger
        """
        return self._logger

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
