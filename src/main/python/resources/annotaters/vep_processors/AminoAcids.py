import pandas as pd
from src.main.python.resources.annotaters.vep_processors.template import Template


class AminoAcids(Template):
    @classmethod
    @property
    def name(cls):
        return 'Amino_acids'

    @classmethod
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['oAA', 'nAA']

    @property
    def oaa(self):
        return self.columns[0]

    @property
    def naa(self):
        return self.columns[1]

    def process(self, dataframe: pd.DataFrame):
        dataframe[self.columns] = dataframe[self.name].str.split('/')
        dataframe[self.naa].fillna(dataframe[self.oaa], inplace=True)
        return dataframe
