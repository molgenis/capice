from abc import ABCMeta, abstractmethod


class ModelSetup(metaclass=ABCMeta):
    """
    Abstract class to act as template for new models that might be
    added in future patches of CAPICE.
    """
    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @staticmethod
    @abstractmethod
    def get_xgb_version():
        """
        Template to distinct models based on the XGBoost version.
        :return: Boolean
        """
        pass

    @staticmethod
    @abstractmethod
    def get_supported_cadd_version():
        """
        Template for the model setup to tell CAPICE
        what CADD version is supported.
        :return: float
        """
        pass

    @staticmethod
    @abstractmethod
    def get_supported_genomebuild_version():
        """
        Template for the model setup to tell CAPICE what genome build is
        supported.
        :return: int
        """
        pass

    @abstractmethod
    def predict(self, data):
        """
        Template method for a model setup to predict and return scores.
        :return: numpy.ndarray
        """
        pass

    @abstractmethod
    def _load_model(self):
        """
        Template method to load in the model once supported values are correct.
        :return: pickled model instance
        """
        pass

    @abstractmethod
    def impute_values(self):
        """
        Template method to tell CAPICE what the impute values are.
        :return: dict
        """
        pass

    @abstractmethod
    def cadd_vars(self):
        """
        Template method to tell CAPICE what all the CADD variants are.
        :return: list
        """
        pass
