from molgenis.capice.main_capice import Main
from molgenis.capice.utilities.enums import Column
from molgenis.capice.utilities.predictor import Predictor
from molgenis.capice.utilities.class_suggestor import ClassSuggestor
from molgenis.capice.validators.post_vep_processing_validator import PostVEPProcessingValidator


class CapicePredict(Main):
    """
    Predict class of CAPICE to call the different modules to impute,
    preprocess and eventually predict a score over a CAPICE annotated file.
    """

    def __init__(self, input_path, model, output_path):
        super().__init__(input_path, output_path)

        # Model.
        self.model = model

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        capice_data = self._load_file(additional_required_features=[Column.gene_name.value,
                                                                    Column.gene_id.value,
                                                                    Column.id_source.value,
                                                                    Column.feature.value])
        capice_data = self.process(loaded_data=capice_data)
        capice_data = self.impute(loaded_data=capice_data, impute_values=self.model.impute_values)
        capice_data = self.preprocess(loaded_data=capice_data,
                                      model_features=self.model.get_booster().feature_names)
        capice_data = self.predict(loaded_data=capice_data)
        capice_data = self.apply_suggested_class(predicted_data=capice_data)
        self._export(dataset=capice_data, output=self.output)

    def process(self, loaded_data):
        """
        Function to process the VEP file to a CAPICE file
        """
        processed_data = super().process(loaded_data)
        validator = PostVEPProcessingValidator(self.model)
        validator.validate_features_present(processed_data)
        return processed_data

    def predict(self, loaded_data):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        predictor = Predictor(self.model)
        capice_data = predictor.predict(loaded_data)
        return capice_data

    @staticmethod
    def apply_suggested_class(predicted_data):
        """
        Method to call the ClassSuggestor
        :return: pandas DataFrame
        """
        suggestor = ClassSuggestor()
        capice_data = suggestor.apply_suggestion(predicted_data)
        return capice_data

