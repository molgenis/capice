import pandas as pd

from molgenis.capice.vep.template import Template
from molgenis.capice.utilities.enums import Column


class SpliceAI(Template):
    def __init__(self):
        super(SpliceAI, self).__init__(
            name='SpliceAI_pred_SYMBOL',
            usable=True
        )

    @property
    def columns(self):
        return ['SpliceAI_pred_SYMBOL_match']

    def _process(self, dataframe: pd.DataFrame):
        dataframe[self.columns] = 0
        dataframe.loc[
            dataframe[dataframe[Column.gene_name.value] == dataframe[self.name]].index, self.columns
        ] = 1
        return dataframe
