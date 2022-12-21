import pandas as pd

from molgenis.capice.vep.template import Template


class AminoAcids(Template):
    def __init__(self):
        super(AminoAcids, self).__init__(
            name='Amino_acids',
            usable=True
        )

    @property
    def columns(self):
        return ['oAA', 'nAA']

    @property
    def oaa(self):
        return self.columns[0]

    @property
    def naa(self):
        return self.columns[1]

    def _process(self, dataframe: pd.DataFrame):
        if dataframe[self.name].str.contains('/', regex=False).any():
            dataframe[self.columns] = dataframe[self.name].str.split('/', expand=True)
            dataframe[self.naa].fillna(dataframe[self.oaa], inplace=True)
        else:
            dataframe[self.oaa] = dataframe[self.name]
            dataframe[self.naa] = dataframe[self.oaa]
        return dataframe
