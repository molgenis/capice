"""
Module Cadd14Grch37 to contain the CADD features present in CADD v1.4 for Genome Build 37 and their 'default' values
for imputing.
"""

from src.main.python.resources.data_files.imputing.impute_values_abstract import TemplateImputeValues


class Cadd14Grch37(TemplateImputeValues):
    def __init__(self):
        super().__init__(
                name='CADD 1.4, GRCh build 37',
                usable=True,
                cadd_version=1.4,
                grch_build=37
        )

    @staticmethod
    def _json_name():
        return 'Cadd14Grch37.json'
