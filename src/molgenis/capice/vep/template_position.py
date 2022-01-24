from abc import abstractmethod

import numpy as np
import pandas as pd

from molgenis.capice.vep.template import Template


class TemplatePosition(Template):
    def __init__(self, name='Template', usable=False):
        super(TemplatePosition, self).__init__(
            name=name,
            usable=usable
        )

    @property
    @abstractmethod
    def columns(self):
        return [None, None]

    @property
    def pos_col(self):
        return self.columns[0]

    def _process(self, dataframe: pd.DataFrame):
        if self.name in dataframe.select_dtypes(include='O'):
            if dataframe[self.name].str.split('/', expand=True).shape[1] > 1:
                dataframe[self.columns] = dataframe[self.name].str.split('/', expand=True)
            else:
                dataframe[self.pos_col] = dataframe[self.name]
                dataframe[self.columns[1]] = np.nan
            dataframe[self.pos_col] = dataframe[self.pos_col].str.replace('?-', '', regex=False)
            dataframe[self.pos_col] = dataframe[self.pos_col].str.replace('-?', '', regex=False)
            dataframe[self.pos_col] = dataframe[self.pos_col].str.split('-', expand=True)[0]

            for column in self.columns:
                dataframe.loc[dataframe[dataframe[column] == ''].index, column] = np.nan
                dataframe[column] = dataframe[column].astype(float)
        else:
            dataframe[self.pos_col] = dataframe[self.name]
            for col in self.columns:
                if col not in dataframe.columns:
                    dataframe[col] = np.nan
        return dataframe
