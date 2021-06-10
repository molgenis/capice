import pandas as pd
from src.main.python.resources.annotaters.vep_processors.template import Template
import numpy as np


class MotifEHIPos(Template):
    @classmethod
    @property
    def name(cls):
        return 'HIGH_INF_POS'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['motifEHIPos']

    def process(self, dataset: pd.DataFrame):
        dataset['motifEHIPos'] = np.where(dataset[self.name] == 'Y', 1, 0)
        return dataset
