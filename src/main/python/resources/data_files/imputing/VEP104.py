"""
Module Cadd14Grch37 to contain the CADD features present in CADD v1.4 for Genome Build 37 and their 'default' values
for imputing.
"""

from src.main.python.resources.data_files.imputing.impute_values_abstract import TemplateImputeValues


class VEP104(TemplateImputeValues):
    def __init__(self):
        super().__init__(
                name='VEP104',
                usable=True,
                vep_version=104.0
        )

    @staticmethod
    def _json_name():
        return 'VEP104.json'
