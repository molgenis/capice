import sys
import xgboost as xgb
from src import VersionError


class CapiceManager:
    class __CapiceManager:
        """
        Class to make a logfile on the progress being made.
        """
        def __init__(self):
            self.version = self._get_python_version()
            self.xgboost_version = self._get_xgboost_version()
            self._threshold = 0.2
            self._set_threshold()
            self._verbose = False

        @staticmethod
        def _get_python_version():
            if sys.version_info[0] < 3:
                raise VersionError('Python 2 is not supported.')
            return sys.version_info[1]

        @staticmethod
        def _get_xgboost_version():
            return xgb.__version__

        def _set_threshold(self):
            if self.version > 6:
                self._threshold = 0.132

        def get_threshold(self):
            return self._threshold

        def set_verbose(self, verbose: bool):
            self._verbose = verbose

        def get_verbose(self):
            return self._verbose

    instance = None

    def get_threshold(self):
        pass

    def set_verbose(self, verbose: bool):
        pass

    def get_verbose(self):
        pass

    def __new__(cls):
        """
        Class method to set CapiceManager instance
        :return: instance
        """
        if not CapiceManager.instance:
            CapiceManager.instance = CapiceManager.__CapiceManager()
        return CapiceManager.instance

    def __init__(self):
        """
        __init__ method to set instance to CapiceManager.__CapiceManager()
        """
        if not CapiceManager.instance:
            CapiceManager.instance = CapiceManager.__CapiceManager()

    def __getattr__(self, name):
        """
        Method to return the value of the named attribute of name
        :param name: str
        :return: str
        """
        return getattr(self.instance, name)
