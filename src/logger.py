"""
    File:         logger.py
    Created:      2019/10/11
    Last Changed:
    Author(s):    M.Vochteloo and R. J. Sietsma

    Copyright 2019 M. Vochteloo and R. J. Sietsma

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import logging
from src.global_manager import CapiceManager
from src.exporter import create_log_export_name


class Logger:
    
    class __Logger:
        def __init__(self):
            self.final_log_loc = None
            self.global_settings = CapiceManager()
            self.log_level = self.set_loglevel()
            self.output_loc = self.global_settings.get_log_loc()
            self.logger = self.load_logger()

        def set_loglevel(self):
            if self.global_settings.get_verbose():
                return logging.NOTSET
            else:
                return logging.WARNING

        def load_logger(self):
            handlers = [logging.StreamHandler()]
            now = self.global_settings.get_now()
            out_file_name = 'capice_{}'.format(now.strftime("%H%M%S%f_%d%m%Y"))
            out_file = create_log_export_name(self.output_loc, out_file_name)
            self.final_log_loc = out_file
            handlers.append(logging.FileHandler(out_file))
            logging.basicConfig(
                level=self.log_level,
                format="%(asctime)s [%(threadName)-10.10s] "
                       "[%(levelname)-4.4s]  "
                       "%(message)s",
                handlers=handlers
            )
            return logging.getLogger(__name__)

        def get_logger(self):
            return self.logger

        def get_log_loc(self):
            return self.final_log_loc
        
    def get_logger(self):
        """
        Function to get the logger instance.
        :return: logger instance
        """
        pass

    def get_log_loc(self):
        """
        Function to get the real location where the logfile is stored for this instance of CAPICE.
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