from src.main.python.resources.annotaters.vep.template import Template
import pandas as pd


class Length(Template):
    def __init__(self):
        super(Length, self).__init__(
            name='Ref',
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe['len_ref'] = dataframe['Ref'].str.len()
        dataframe['len_alt'] = dataframe['Alt'].str.len()
        dataframe['Length'] = (
                    dataframe[['len_ref', 'len_alt']].max(axis=1) - 1)
        dataframe.drop(columns=['len_ref', 'len_alt'], inplace=True)
        return dataframe

    @property
    def drop(self):
        return False
