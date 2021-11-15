import numpy as np
import pandas as pd
from src.main.python.vep.template import Template


class MotifEHIPos(Template):
    def __init__(self):
        super(MotifEHIPos, self).__init__(
            name='HIGH_INF_POS',
            usable=True
        )

    def process(self, dataset: pd.DataFrame):
        dataset['motifEHIPos'] = np.where(dataset[self.name] == 'Y', 1, 0)
        return dataset
