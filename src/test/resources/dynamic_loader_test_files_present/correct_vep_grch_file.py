class CorrectVEPFile:
    @property
    def name(self):
        return 'Correct_VEP_GRCh'

    @property
    def usable(self):
        return True

    @property
    def supported_vep_version(self):
        return 104.0

    @property
    def supported_grch_build(self):
        return 37

    @staticmethod
    def some_function():
        return 'SomeVeryUniqueString'
