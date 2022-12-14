class ModelValidator:
    @staticmethod
    def validate_has_required_attributes(model):
        """
        Function to validate if the required attributes CAPICE_version,
        impute_values and predict_proba are present.
        """
        required_attributes = ['CAPICE_version', 'vep_features',
                               'processable_features', 'predict_proba']
        for attribute in required_attributes:
            if attribute not in dir(model):
                raise AttributeError(f'Unable to locate attribute {attribute} in model file!')
