import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities import check_if_in_list


class PostVEPProcessingValidator:
    def __init__(self):
        self.log = Logger().logger

    def validate_features_present(self, datafile: pd.DataFrame, vep_features: list[list[str]]) -> \
            None:
        """
        Validator to see if all features that should be present after the
        ManualVEPProcessor are present.
        Args:
            datafile:
                Pandas Dataframe over which the feature presence validation should happen.
            vep_features:
                List of lists of expected output ManualVEPProcesing features as saved in the
                model.vep_features.values()
        Raises:
            KeyError:
                Raises KeyError when output VEP feature is not present within datafile.
        """
        features_not_present = check_if_in_list(vep_features, datafile.columns)
        if len(features_not_present) > 0:
            error_message = 'Detected required feature(s) %s not ' \
                            'present within VEP processed input file!'
            self.log.critical(error_message, ', '.join(features_not_present))
            raise KeyError(error_message % ', '.join(features_not_present))
