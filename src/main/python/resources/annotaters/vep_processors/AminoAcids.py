from src.main.python.resources.annotaters.vep_processors.template import Template
import math


class AminoAcids(Template):
    @classmethod
    @property
    def name(cls):
        return 'Amino_acids'

    @classmethod
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['oAA', 'nAA']

    def process(self, value):
        subset = value[AminoAcids.name]
        return_list = []
        if not math.isnan(subset):
            aa = subset.split('/')
            if len(aa) == 2:
                return_list += aa
            else:
                return_list += [aa[0], aa[0]]
        else:
            return_list = [None, None]
        return return_list
