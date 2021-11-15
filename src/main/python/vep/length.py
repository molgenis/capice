import pandas as pd
from src.main.python.vep.template import Template
from src.main.python.utilities.sections import Column


class Length(Template):
    def __init__(self):
        super(Length, self).__init__(
            name=Column.ref.value,
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe['len_ref'] = dataframe[Column.ref.value].str.len()
        dataframe['len_alt'] = dataframe[Column.alt.value].str.len()
        dataframe['Length'] = (
                    dataframe[['len_ref', 'len_alt']].max(axis=1) - 1)
        dataframe.drop(columns=['len_ref', 'len_alt'], inplace=True)
        return dataframe

    @property
    def drop(self):
        return False
