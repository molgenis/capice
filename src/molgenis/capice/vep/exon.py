from molgenis.capice.vep.template_exon_intron import TemplateExonIntron


class Exon(TemplateExonIntron):
    def __init__(self):
        super(Exon, self).__init__(
            name='Exon',
            usable=True
        )

    @property
    def columns(self):
        return ['Exon_number', 'Exon_number_affected', 'Exon_total']
