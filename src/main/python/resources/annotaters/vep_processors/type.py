from src.main.python.resources.annotaters.vep_processors.template import Template
import pandas as pd


class Type(Template):
    def __init__(self):
        super(Type, self).__init__(
            name='Ref',
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe.loc[dataframe[dataframe['Ref'].str.len() == dataframe['Alt'].str.len()].index, 'Type'] = 'SNV'
        dataframe.loc[dataframe[dataframe['Ref'].str.len() > dataframe['Alt'].str.len()].index, 'Type'] = 'DEL'
        dataframe.loc[dataframe[dataframe['Ref'].str.len() < dataframe['Alt'].str.len()].index, 'Type'] = 'INS'
        return dataframe

    @property
    def drop(self):
        return False
