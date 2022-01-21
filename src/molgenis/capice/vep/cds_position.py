from molgenis.capice.vep.template_position import TemplatePosition


class CDSPosition(TemplatePosition):
    def __init__(self):
        super(CDSPosition, self).__init__(
            name='CDS_position',
            usable=True
        )

    @property
    def columns(self):
        return ['CDSpos', 'relCDSpos']
