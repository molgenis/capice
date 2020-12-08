

class CapiceManager:
    class __CapiceManager:
        """
        Class to make a logfile on the progress being made.
        """
        def __init__(self):
            self.threshold = None
            self.verbose = False
            self.log_loc = None
            self.genome_build = None
            self.cadd_version = None
            self.force = False

        def set_log_loc(self, log_loc: str):
            self.log_loc = log_loc

        def get_log_loc(self):
            return self.log_loc

        def set_threshold(self, threshold: float):
            self.threshold = threshold

        def get_threshold(self):
            return self.threshold

        def set_grch_build(self, grch_build: int):
            self.genome_build = grch_build

        def get_grch_build(self):
            return self.genome_build

        def set_cadd_version(self, cadd_version: float):
            self.cadd_version = cadd_version

        def get_cadd_version(self):
            return self.cadd_version

        def set_force(self, force: bool):
            self.set_force(force)

        def get_force(self):
            return self.force

        def set_verbose(self, verbose: bool):
            self.verbose = verbose

        def get_verbose(self):
            return self.verbose

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

    def set_threshold(self, threshold: float):
        """
        Function to globally set the threshold of CAPICE.
        :param threshold: float
        """
        pass

    def get_threshold(self):
        """
        Get the threshold value.
        :return: float
        """
        pass

    def set_grch_build(self, grch_build: int):
        """
        Function to set the Genome GRCh build globally
        :param grch_build: integer
        """
        pass

    def get_grch_build(self):
        """
        Function to get the global Genome GRCh build
        :return: int
        """
        pass

    def set_cadd_version(self, cadd_version: float):
        """
        Function to set the CADD annotation version globally
        :param cadd_version: float
        """
        pass

    def get_cadd_version(self):
        """
        Function to get the global CADD annotation version
        :return: float
        """
        pass

    def set_force(self, force: bool):
        """
        Function to set the force output, overwrites any result that is already there.
        :param force: bool
        """
        pass

    def get_force(self):
        """
        Function to get the global force output boolean
        :return: bool
        """
        pass

    def set_verbose(self, verbose: bool):
        """
        Set the verbose true (log everything to file) or
        false (only log warnings and errors).
        :param verbose: bool
        """
        pass

    def get_verbose(self):
        """
        Get the verbose level.
        :return: bool
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
