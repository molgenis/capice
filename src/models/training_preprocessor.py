from src.models.model_abstract import TemplateSetup


class TrainPreprocessor(TemplateSetup):
    @staticmethod
    def get_name():
        return "Preprocessor for training"

    @staticmethod
    def is_usable():
        return False

    @staticmethod
    def get_supported_cadd_version():
        return None

    @staticmethod
    def get_supported_genomebuild_version():
        return None

    @staticmethod
    def _get_model_loc():
        return None
