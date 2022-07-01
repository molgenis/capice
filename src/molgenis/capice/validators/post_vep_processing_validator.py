from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities.column_utils import ColumnUtils


class PostVEPProcessingValidator:
    def __init__(self, model):
        self.model = model
        self.log = Logger().logger

    def validate_features_present(self, datafile):
        """
        Validator to see if all features within the model impute values are
        presently processed.
        """
        column_utils = ColumnUtils()
        column_utils.set_specified_columns(self.model.impute_values.keys())
        features_not_present = column_utils.get_missing_diff_with(datafile.columns)
        if len(features_not_present) > 0:
            error_message = 'Detected required feature(s) %s not ' \
                            'present within VEP processed input file!'
            self.log.critical(error_message, ', '.join(features_not_present))
            raise KeyError(error_message % ', '.join(features_not_present))
