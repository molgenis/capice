"""
Module VEP104 to contain the features present in the model for VEP104 and
Genome Build 37 and their 'default' values for imputing.
"""

from src.main.python.resources.data_files.imputing.impute_values_abstract \
    import TemplateImputeValues


class VEP104(TemplateImputeValues):
    def __init__(self):
        super().__init__(
            name='VEP104',
            usable=True,
            vep_version=104.0,
            grch_build=37
        )

    @staticmethod
    def _json_name():
        return 'VEP104.json'
