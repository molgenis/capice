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
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.utilities.utilities import SetCustomLoggingFilter


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
            self.stdout_loglevels = []
            self.stderr_loglevels = [logging.CRITICAL]
            self.set_loglevels()
            self.logger = None
            if self.logger is None:
                self.load_logger()

        def set_loglevels(self):
            """
            Function to set the log level at where messages are printed or
            logged. For more information, see:
            https://docs.python.org/3/library/logging.html#logging-levels
            :return: logging level
            """
            if not self.global_settings.critical_logging_only:
                self.stdout = True
                self.stderr_loglevels += [logging.WARNING, logging.ERROR]
                self.stdout_loglevels.append(logging.INFO)
                if self.global_settings.verbose:
                    self.stdout_loglevels.append(logging.DEBUG)

        def load_logger(self):
            """
            Function to set up the logger instance with the correct format and
            filename.

            :return: logger instance
            """
            # Making a root logger to make sure the level is set correctly.
            logger = logging.getLogger()
            # Now renaming it to CAPICE.
            logger.name = 'CAPICE'

            formatter = logging.Formatter("%(asctime)s "
                                          "[%(name)s] "
                                          "[%(filename)s] "
                                          "[%(funcName)s] "
                                          "[%(levelname)-4.4s]  "
                                          "%(message)s")

            # Setting the log level to debug, but with an applied filter
            logger.setLevel(logging.DEBUG)

            # sys.stdout (if not critical logging only)
            if self.stdout:
                stdout_handler = logging.StreamHandler(sys.stdout)
                stdout_handler.setLevel(logging.DEBUG)
                stdout_handler.addFilter(
                    SetCustomLoggingFilter(
                        self.stdout_loglevels
                    )
                )
                stdout_handler.setFormatter(formatter)
                logger.addHandler(stdout_handler)

            # sys.stderr
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(logging.WARNING)
            stderr_handler.addFilter(
                SetCustomLoggingFilter(
                    self.stderr_loglevels
                )
            )
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
