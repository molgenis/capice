"""
File specific to preprocessing of training files used by train_model.py.
"""

from src.main.python.resources.models.model_abstract import TemplateSetup


class TrainPreprocessor(TemplateSetup):
    def __init__(self):
        super().__init__(
            name='Preprocessor for training',
            usable=False,
            vep_version=None,
            grch_build=None
        )

    @staticmethod
    def _get_model_loc():
        return None
