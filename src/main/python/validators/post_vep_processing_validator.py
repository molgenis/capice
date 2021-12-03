from src.main.python.core.logger import Logger


class PostVEPProcessingValidator:
    def __init__(self, model):
        self.model = model
        self.log = Logger().logger

    def validate_features_present(self, datafile):
        """
        Validator to see if all features within the model impute values are
        presently processed.
        """
        features_not_present = []
        for feature in self.model.impute_values.keys():
            if feature not in datafile.columns:
                features_not_present.append(feature)
        if len(features_not_present) > 0:
            error_message = 'Detected required feature(s) %s not ' \
                            'present within VEP processed input file!'
            self.log.critical(error_message, ', '.join(features_not_present))
            raise KeyError(error_message % ', '.join(features_not_present))
