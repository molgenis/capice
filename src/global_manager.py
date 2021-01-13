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
            self.cadd_version = None
            self.grch_build = None
            self.force = False
            self.cadd_features = []
            self.full_cadd_features = []

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

        def set_cadd_version(self, cadd_version):
            self.cadd_version = cadd_version

        def get_cadd_version(self):
            return self.cadd_version

        def set_grch_build(self, grch_build):
            self.grch_build = grch_build

        def get_grch_build(self):
            return self.grch_build

        def set_cadd_features(self, cadd_features):
            self.cadd_features = cadd_features

        def get_cadd_features(self):
            return self.cadd_features

        def set_full_cadd_features(self, cadd_features):
            self.full_cadd_features = cadd_features

        def get_full_cadd_features(self):
            return self.full_cadd_features

        def set_force(self, force):
            self.force = force

        def get_force(self):
            return self.force

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

    def set_cadd_version(self, cadd_version):
        """
        Function to set the globally available CADD version
        :param cadd_version: float
        """
        pass

    def get_cadd_version(self):
        """
        Function to get the globally available CADD version
        :return: float
        """
        pass

    def set_grch_build(self, grch_build):
        """
        Function to set the globally available GRCh build
        :param grch_build: int
        """
        pass

    def get_grch_build(self):
        """
        Function to get the globally available GRCh build
        :return: int
        """
        pass

    def set_cadd_features(self, cadd_features):
        """
        Function to set the globally available cadd_features list required for both imputing and preprocessing
        :param cadd_features: list
        """
        pass

    def get_cadd_features(self):
        """
        Function to get the globally available cadd_features list required for both imputing and preprocessing
        :return: list
        """
        pass

    def set_full_cadd_features(self, cadd_features):
        """
        Function to set the globally available cadd features list, including #Chr, Pos and FeatureID
        :param cadd_features: list
        """
        pass

    def get_full_cadd_features(self):
        """
        Similar function to get_cadd_features(), but now includes additional columns to keep and save
        :return: list
        """
        pass

    def set_force(self, force):
        """
        Function to set the globally force argument to overwrite an existing CAPICE output file
        :param force: bool
        """
        pass

    def get_force(self):
        """
        Function to get the globally force argument whenever overwriting an existing CAPICE output file is allowed
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
