import pandas as pd

from src.main.python.resources.annotaters.vep_processors.template import Template
import numpy as np


class MotifName(Template):
    @classmethod
    @property
    def name(cls):
        return 'MOTIF_NAME'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['motifECount', 'motifEName']

    def process(self, dataframe: pd.DataFrame):
        dataframe['motifEName'] = dataframe[self.name]
        dataframe['motifECount'] = np.where(dataframe[self.name].isna(), None, '1')
        return dataframe
