import pandas as pd
from src.main.python.resources.annotaters.vep_processors.template import Template


class MotifEScoreChange(Template):
    @classmethod
    @property
    def name(cls):
        return 'MOTIF_SCORE_CHANGE'

    @classmethod
    @property
    def usable(cls):
        return True

    def process(self, dataset: pd.DataFrame):
        dataset['motifEScoreChng'] = dataset[self.name]
        return dataset
