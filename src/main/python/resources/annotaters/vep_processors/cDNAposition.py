from src.main.python.resources.annotaters.vep_processors.template import Template
import math


class CDNAPosition(Template):
    @classmethod
    @property
    def name(cls):
        return 'cDNA_position'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['cDNApos', 'relcDNApos']

    @property
    def get_name(self):
        return CDNAPosition.name

    def process(self, value):
        return_list = []
        subset = value[self.get_name]
        if not math.isnan(subset):
            pos, length = subset.split('/')
            pos = pos.replace('?-', '').replace('-?', '').split('-')[0]
            if pos != '':
                return_list += [pos, float(length)]
            else:
                return_list += [None, None]
        else:
            return_list += [None, None]
        return return_list
