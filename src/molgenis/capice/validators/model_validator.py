import xgboost


class ModelValidator:
    def __init__(self, parser):
        self.parser = parser

    def validate_is_xgb_classifier(self, model):
        """
        Function to validate if loaded pickle is of xgb.XGBClassifier class.
        """
        if not isinstance(model, xgboost.XGBClassifier):
            self.parser.error('Given pickle is not a XGBClassifier class!')

    def validate_has_required_attributes(self, model):
        """
        Function to validate if the required attributes CAPICE_version, impute_values and predict_proba are present.
        """
        required_attributes = ['CAPICE_version', 'impute_values', 'predict_proba']
        for attribute in required_attributes:
            if attribute not in dir(model):
                self.parser.error(f'Unable to locate attribute {attribute} in model file!')
