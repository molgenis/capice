import pandas as pd

from molgenis.capice.vep.template_sift_polyphen import TemplateSiftPolyPhen


class SIFT(TemplateSiftPolyPhen):
    def __init__(self):
        super(SIFT, self).__init__(
            name='SIFT',
            usable=True
        )

    @property
    def columns(self):
        return ['SIFTcat', 'SIFTval']

    def apply_label(self, dataframe: pd.DataFrame):
        """
        Under the 0.05 should be deleterious, everything else should be tolerated (if not nan)
        """
        dataframe.loc[
            dataframe[dataframe[self.name].notnull()].index, self.columns[0]] = 'tolerated'
        dataframe.loc[
            dataframe[dataframe[self.name] <= 0.05].index, self.columns[0]] = 'deleterious'
        return dataframe
