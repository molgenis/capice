import pandas as pd
from src.main.python.resources.annotaters.vep.template import Template
import numpy as np


class MotifName(Template):
    def __init__(self):
        super(MotifName, self).__init__(
            name='MOTIF_NAME',
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe['motifEName'] = dataframe[self.name]
        dataframe['motifECount'] = np.where(dataframe[self.name].isna(), 0, 1)
        return dataframe
