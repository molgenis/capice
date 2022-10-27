from abc import abstractmethod

import pandas as pd

from molgenis.capice.vep.template import Template


class TemplateExonIntron(Template):
    def __init__(self, name='Template', usable=False):
        super(TemplateExonIntron, self).__init__(
            name=name,
            usable=usable
        )

    @property
    @abstractmethod
    def columns(self):
        return [None, None]

    @property
    def get_number_column(self):
        return self.columns[0]

    def _process(self, dataframe: pd.DataFrame):
        dataframe[self.columns] = dataframe[self.name].str.split('/', expand=True)
        dataframe[self.get_number_column] = dataframe[self.get_number_column].str.split('-', expand=True)[0]
        for column in self.columns:
            dataframe[column] = dataframe[column].astype('Int64')
        return dataframe
