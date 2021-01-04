from datetime import datetime


class CapiceManager:
    class __CapiceManager:
        """
        Class to make a logfile on the progress being made.
        """
        def __init__(self):
            self.log_loc = None
            self.now = datetime.now()

        def set_log_loc(self, log_loc: str):
            self.log_loc = log_loc

        def get_log_loc(self):
            return self.log_loc

        def get_now(self):
            return self.now

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

    def get_now(self):
        """
        Get the datetime now instance to keep log and output the same
        :return: datetime
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
