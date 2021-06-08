from src.main.python.resources.annotaters.vep_processors.template import Template
import math


class Domain(Template):
    @classmethod
    @property
    def name(cls):
        return 'DOMAINS'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['Domain']

    def process(self, value):
        subset = value[Domain.name]
        return_value = None
        if not math.isnan(subset):
            return_value = 'other'
            for fields in subset.split('&'):
                pass

