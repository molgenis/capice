from molgenis.capice.vep.template_exon_intron import TemplateExonIntron


class Intron(TemplateExonIntron):
    def __init__(self):
        super(Intron, self).__init__(
            name='Intron',
            usable=True
        )

    @property
    def columns(self):
        return ['Intron_number', 'Intron_total']
