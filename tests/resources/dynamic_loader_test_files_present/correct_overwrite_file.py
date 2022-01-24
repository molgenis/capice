class CorrectOverwriteFile:
    @property
    def name(self):
        return 'Correct_Overwrite'

    @property
    def usable(self):
        return True

    @property
    def supported_vep_version(self):
        return None

    @property
    def supported_grch_build(self):
        return None

    @staticmethod
    def some_function():
        return 'SomeVeryUniqueString_butdifferent'
