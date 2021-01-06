from datetime import datetime


class CapiceManager:
    class __CapiceManager:
        """
        Class to make a logfile on the progress being made.
        """
        def __init__(self):
            self.log_loc = None
            self.now = None
            self.overwrite_impute = None
            self.overwrite_model = None

        def set_log_loc(self, log_loc: str):
            self.log_loc = log_loc

        def get_log_loc(self):
            return self.log_loc

        def set_now(self):
            self.now = datetime.now()

        def get_now(self):
            return self.now

        def set_overwrite_impute(self, overwrite_impute):
            self.overwrite_impute = overwrite_impute

        def get_overwrite_impute(self):
            return self.overwrite_impute

        def set_overwrite_model(self, overwrite_model):
            self.overwrite_model = overwrite_model

        def get_overwrite_model(self):
            return self.overwrite_model

    instance = None

    def set_log_loc(self, log_loc):
        """
        Function to set the output of the logfile.
        :param log_loc: str, path of or to logfile
        """
        pass

    def get_log_loc(self):
        """
        Function to get the logfile location.
        :return: str
        """
        pass

    def set_now(self):
        """
        Initial function of CAPICE manager to set a datetime instance consistent across the entire program.
        """
        pass

    def get_now(self):
        """
        Get the datetime now instance to keep log and output the same
        :return: datetime
        """
        pass

    def set_overwrite_impute(self, overwrite_impute):
        """
        Function to set the global variable of forcing a specific imputing file
        :param overwrite_impute: None or string
        """
        pass

    def get_overwrite_impute(self):
        """
        Function to get the global variable of forcing a specific imputing file
        :return: None or string
        """
        pass

    def set_overwrite_model(self, overwrite_model):
        """
        Function to set the global variable of forcing a specific model file
        :param overwrite_model: None or string
        """
        pass

    def get_overwrite_model(self):
        """
        Function to get the global variable of forcing a specific model file
        :return: Nopne or string
        """
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
