import pandas as pd
from src.main.python.resources.enums.sections import Column
from src.main.python.resources.processors.vep.template import Template


class Type(Template):
    def __init__(self):
        super(Type, self).__init__(
            name=Column.ref.value,
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe.loc[
            dataframe[
                dataframe[Column.ref.value].str.len() == dataframe[
                    Column.alt.value].str.len()].index,
            'Type'] = 'SNV'
        dataframe.loc[
            dataframe[
                dataframe[Column.ref.value].str.len() > dataframe[
                    Column.alt.value].str.len()].index,
            'Type'] = 'DEL'
        dataframe.loc[
            dataframe[
                dataframe[Column.ref.value].str.len() < dataframe[
                    Column.alt.value].str.len()].index,
            'Type'] = 'INS'
        return dataframe

    @property
    def drop(self):
        return False
