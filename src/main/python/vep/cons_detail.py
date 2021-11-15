import pandas as pd
from src.main.python.vep.template import Template


class ConsDetail(Template):
    def __init__(self):
        super(ConsDetail, self).__init__(
            name='Consequence',
            usable=True
        )

    @property
    def replace_empty(self):
        return ['_variant', '_region', '_gene', '_transcript']

    @property
    def drop(self):
        return False

    def process(self, dataframe: pd.DataFrame):
        subset = dataframe[self.name].str.split('&', expand=True)
        for column in subset.columns:
            for string in self.replace_empty:
                subset[column] = subset[column].str.replace(
                    string, '', regex=False)
        subset.loc[subset[subset.notnull().all(axis=1)].index, 0] = subset[
            subset.notnull().all(axis=1)].agg(','.join, axis=1)
        dataframe['ConsDetail'] = subset[0]
        return dataframe
