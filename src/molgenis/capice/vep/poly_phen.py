import pandas as pd

from molgenis.capice.vep.template_sift_polyphen import TemplateSiftPolyPhen


class PolyPhen(TemplateSiftPolyPhen):
    def __init__(self):
        super(PolyPhen, self).__init__(
            name='PolyPhen',
            usable=True
        )

    @property
    def columns(self):
        return ['PolyPhenCat', 'PolyPhenVal']

    def apply_label(self, dataframe: pd.DataFrame):
        """
        Under the 0.445 should be benign, between 0.445 and 0.908 should be possibly damaging,
        everything else should be probably damaging (if not nan).
        """
        dataframe.loc[dataframe[dataframe[self.name].notnull()].index, self.columns[0]] = 'benign'
        dataframe.loc[
            dataframe[dataframe[self.name] > 0.445].index, self.columns[0]] = 'possibly_damaging'
        dataframe.loc[
            dataframe[dataframe[self.name] > 0.908].index, self.columns[0]] = 'probably_damaging'
        return dataframe
