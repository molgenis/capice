import pandas as pd

from molgenis.capice.vep.template import Template
from molgenis.capice.utilities.enums import Column


class Length(Template):
    def __init__(self):
        super(Length, self).__init__(
            name=Column.ref.value,
            usable=True
        )

    @property
    def columns(self):
        return ['Length']

    def _process(self, dataframe: pd.DataFrame):
        dataframe = dataframe.join(
            pd.DataFrame(
                abs(dataframe[Column.ref.value].str.len() - dataframe[Column.alt.value].str.len()),
                columns=self.columns
            )
        )
        return dataframe

    @property
    def drop(self):
        return False
