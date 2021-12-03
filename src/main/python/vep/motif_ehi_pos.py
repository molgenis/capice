import numpy as np
import pandas as pd
from src.main.python.vep.template import Template


class MotifEHIPos(Template):
    def __init__(self):
        super(MotifEHIPos, self).__init__(
            name='HIGH_INF_POS',
            usable=True
        )

    @property
    def columns(self):
        return ['motifEHIPos']

    def process(self, dataframe: pd.DataFrame):
        return self._process(dataframe)

    def _process(self, dataset: pd.DataFrame):
        dataset[self.columns] = np.where(dataset[self.name] == 'Y', 1, 0)
        return dataset
