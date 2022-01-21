from abc import abstractmethod

import numpy as np
import pandas as pd

from molgenis.capice.vep.template import Template


class TemplateSiftPolyPhen(Template):
    def __init__(self, name='Template', usable=False):
        super(TemplateSiftPolyPhen, self).__init__(
            name=name,
            usable=usable
        )

    @property
    @abstractmethod
    def columns(self):
        return [None, None]

    @abstractmethod
    def apply_label(self, dataframe: pd.DataFrame):
        return dataframe

    def _process(self, dataframe: pd.DataFrame):
        dataframe[self.columns[1]] = dataframe[self.name]
        dataframe[self.columns[0]] = np.nan
        dataframe = self.apply_label(dataframe)
        return dataframe
