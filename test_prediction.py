import unittest
from test_global import TestGlobal


class Test(TestGlobal):
    """
    Testing module for CAPICE predictions
    """
    def test_unit_prediction(self):
        print('Prediction (unit)')
        for file, overwrite in self.processing_files_overwrite.items():
            preprocessing_instance, processed_file = self.prepare_upon_preprocessing(model=overwrite, file=file)
            self.main.predict(loaded_cadd_data=processed_file, preprocessing_instance=preprocessing_instance)

    def test_component_prediction(self):
        print('Prediction (component)')
        for file, overwrite in self.processing_files_overwrite.items():
            preprocessing_instance, processed_file = self.prepare_upon_preprocessing(model=overwrite, file=file)
            prediction = self.main.predict(loaded_cadd_data=processed_file,
                                           preprocessing_instance=preprocessing_instance)
            # Combined sum of the prediction score should be higher than 0
            self.assertGreater(prediction['probabilities'].sum(), 0)


if __name__ == '__main__':
    unittest.main()
