import pandas as pd
from src.main.python.vep.template import Template
from src.main.python.utilities.enums import Column


class Length(Template):
    def __init__(self):
        super(Length, self).__init__(
            name=Column.ref.value,
            usable=True
        )

    def process(self, dataframe: pd.DataFrame):
        dataframe['Length'] = abs(
            dataframe[Column.ref.value].str.len() - dataframe[Column.alt.value].str.len()
        )
        return dataframe

    @property
    def drop(self):
        return False
