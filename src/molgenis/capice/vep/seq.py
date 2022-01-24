import pandas as pd

from molgenis.capice.vep.template import Template


class SEQ(Template):
    def __init__(self):
        super(SEQ, self).__init__(
            name='Seq',
            usable=False
        )

    @property
    def columns(self):
        return ['GC', 'CpG']

    @staticmethod
    def _calculate_g_c_n(dataframe, name):
        c = dataframe[name].str.count('C')
        g = dataframe[name].str.count('G')
        n = dataframe[name].str.count('N')
        return (c + g + n * 0.41) / dataframe[name].str.len()

    @staticmethod
    def _calculate_cg_n(dataframe, name):
        cg = dataframe[name].str.count('CG')
        n = dataframe[name].str.count('N')
        return (cg + n * 0.01) / (dataframe[name].str.len() - 1) * 2

    def _process(self, dataframe: pd.DataFrame):
        dataframe[self.columns[0]] = self._calculate_g_c_n(dataframe, self.name)
        dataframe[self.columns[1]] = self._calculate_cg_n(dataframe, self.name)
        return dataframe
