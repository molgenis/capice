import numpy as np
import pandas as pd
from src.main.python.vep.template import Template


class MotifName(Template):
    def __init__(self):
        super(MotifName, self).__init__(
            name='MOTIF_NAME',
            usable=True
        )

    @property
    def columns(self):
        return ['motifEName', 'motifECount']

    def process(self, dataframe: pd.DataFrame):
        return self._process(dataframe)

    def _process(self, dataframe: pd.DataFrame):
        dataframe[self.columns[0]] = dataframe[self.name]
        dataframe[self.columns[1]] = np.where(dataframe[self.name].isna(), 0, 1)
        return dataframe
