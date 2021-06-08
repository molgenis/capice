from src.main.python.resources.annotaters.vep_processors.template import Template


class MotifName(Template):
    @classmethod
    @property
    def name(cls):
        return 'MOTIF_NAME'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['motifECount', 'motifEName']

    def process(self, value):
        return_list = []
        if value[MotifName.name] is not None:
            return_list.append('1')
            return_list.append(value[MotifName])
        else:
            return_list = [None, None]
        return return_list
