from src.main.python.resources.annotaters.vep_processors.template import Template


class SEQ(Template):
    @classmethod
    @property
    def name(cls):
        return 'Seq'

    @classmethod
    @property
    def usable(cls):
        return True

    @property
    def columns(self):
        return ['GC', 'CpG']

    def process(self, value):
        return_value = []
        seq = value[SEQ.name]
        seq_len = len(seq)
        num_n = seq.count('N')
        return_value.append((seq.count('C') + seq.count('G') + num_n * 0.41) / seq_len)
        return_value.append((seq.count('CG') + num_n * 0.01) / (seq_len - 1) * 2)
        return return_value
