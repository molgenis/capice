from datetime import datetime
import logging
from CAPICE_scripts.src.utilities.utilities import get_project_root_dir,\
    prepare_dir
from CAPICE_scripts.src.global_manager import CapiceManager


class Logger:
    
    class __Logger:
        def __init__(self):
            self._global_settings = CapiceManager()
            self._log_level = self._set_loglevel()
            pass

        def _set_loglevel(self):
            if self._global_settings.get_verbose():
                return logging.NOTSET
            else:
                return logging.WARNING
        
    def get_logger(self):
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