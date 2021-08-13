import pandas as pd
from src.main.python.resources.annotaters.vep.template import Template


class SEQ(Template):
    def __init__(self):
        super(SEQ, self).__init__(
            name='Seq',
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe['GC'] = (dataframe[self.name].str.count('C') + dataframe[
            self.name].str.count('G') + dataframe[
                               self.name].str.count('N') * 0.41) / dataframe[
                              self.name].str.len()
        dataframe['CpG'] = (dataframe[self.name].str.count('CG') + dataframe[
            self.name].str.count('N') * 0.01) / (
                                   dataframe[self.name].str.len() - 1) * 2
        return dataframe
