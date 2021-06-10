import pandas as pd
from src.main.python.resources.annotaters.vep_processors.template import Template


class CDNAPosition(Template):
    @classmethod
    @property
    def name(cls):
        return 'cDNA_position'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['cDNApos', 'relcDNApos']

    @property
    def pos_col(self):
        return self.columns[0]

    def process(self, dataframe: pd.DataFrame):
        dataframe[self.columns] = dataframe[self.name].str.split('/', expand=True)
        dataframe[self.pos_col] = dataframe[self.pos_col].str.replace('?-', '', regex=False)
        dataframe[self.pos_col] = dataframe[self.pos_col].str.replace('-?', '', regex=False)
        dataframe[self.pos_col] = dataframe[self.pos_col].str.split('-', expand=True)[0]
        for column in self.columns:
            dataframe[column] = dataframe[column].astype(float)
        return dataframe
