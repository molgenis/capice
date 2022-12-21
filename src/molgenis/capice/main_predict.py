from molgenis.capice.main_capice import Main
from molgenis.capice.utilities.enums import Column
from molgenis.capice.utilities.predictor import Predictor
from molgenis.capice.utilities.class_suggestor import ClassSuggestor
from molgenis.capice.validators.predict_validator import PredictValidator
from molgenis.capice.validators.post_vep_processing_validator import PostVEPProcessingValidator


class CapicePredict(Main):
    """
    Predict class of CAPICE to call the different modules to impute,
    process and eventually predict a score over a CAPICE annotated file.
    """

    def __init__(self, input_path, model, output_path, output_given):
        super().__init__(input_path, output_path, output_given)

        # Model.
        self.model = model

    def run(self):
        """
        Function to make CAPICE run in a prediction matter.
        """
        capice_data = self._load_file(additional_required_features=[Column.gene_name.value,
                                                                    Column.gene_id.value,
                                                                    Column.id_source.value,
                                                                    Column.feature.value,
                                                                    Column.feature_type.value])
        capice_data = self.process(
            loaded_data=capice_data,
            process_features=list(self.model.vep_features.keys())
        )[0]
        PostVEPProcessingValidator().validate_features_present(
            capice_data, self.model.vep_features.values()
        )
        capice_data = self.categorical_process(
            loaded_data=capice_data,
            processing_features=self.model.processable_features,
            train_features=None
        )[0]
        capice_data = self.predict(loaded_data=capice_data)
        capice_data = self.apply_suggested_class(predicted_data=capice_data)
        self._export(dataset=capice_data, output=self.output)

    def predict(self, loaded_data):
        """
        Function to call the correct model to predict CAPICE scores
        :return: pandas DataFrame
        """
        validator = PredictValidator()
        validator.validate_data_predict_ready(loaded_data, self.model)
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
