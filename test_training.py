import unittest
import os
from datetime import datetime
import pickle

from src.main_train import Train
from src.main import Main
from src.global_manager import CapiceManager
from src.utilities.utilities import get_project_root_dir
from test_global import setup_class, teardown_class, __program__, __version__, __author__


class Test(unittest.TestCase):
    """
    Testing module for both creating new CAPICE like models
    """
    @classmethod
    def setUpClass(cls):

        cls.output_dir = setup_class()

        cls.manager = CapiceManager()
        cls.manager.now = datetime.now()
        cls.manager.disable_logfile = True
        cls.manager.critical_logging_only = True
        cls.manager.verbose = False

        test_file = 'train_dataset.tsv.gz'  # Replace with the name of the file you want to test

        # Replace with the version that you want to use and is supported in the imputing files
        impute_overwrite = "CADD 1.4, GRCh build 37"

        input_file = os.path.join(get_project_root_dir(), 'CAPICE_example', test_file)

        cls.manager.overwrite_impute = impute_overwrite

        cls.main = Train(__program__=__program__,
                         __version__=__version__,
                         __author__=__author__,
                         input_loc=input_file,
                         output_loc=cls.output_dir,
                         balance=False,  # Do need to test
                         default=False,  # Do need to test
                         specified_default=False,  # Do need to test
                         split=False,  # Do need to test
                         early_exit=False,
                         train_test_size=0.2  # Do need to test
                         )

        cls.processing_pipeline = Main(
            __program__=__program__,
            __version__=__version__,
            __author__=__author__,
            input_loc=input_file,
            output_loc=None,
            genome_build=None,
            cadd_build=None
        )

        print('Set up complete, testing cases.')

    @classmethod
    def tearDownClass(cls):
        teardown_class()

    def setUp(self):
        print('----------------------------------------------------------------------')
        print('Performing test:')

    def tearDown(self):
        print('Resetting arguments.')
        print('----------------------------------------------------------------------')

    def test_integration_training(self):
        print('Training (integration)\n')
        self.main._integration_test = True
        self.main.main()
        output_filename = "randomized_search_cv_" + self.manager.now.strftime("%H%M%S%f_%d%m%Y") + '.pickle.dat'
        output_loc = os.path.join(self.output_dir, output_filename)
        with open(output_loc, 'rb') as model_dat:
            model = pickle.load(model_dat)
        class_used = str(model.__class__).split("'")[1]
        self.assertEqual('sklearn.model_selection._search.RandomizedSearchCV', class_used)
        best_model = str(model.best_estimator_.__class__).split("'")[1]
        self.assertEqual('xgboost.sklearn.XGBClassifier', best_model)

    def test_component_preprocessing(self):
        print('Preprocessing (train) (component)')
        loaded_file = self.processing_pipeline.load_file()
        imputed_file = self.processing_pipeline.impute(loaded_cadd_data=loaded_file)
        preprocessor, preprocessed_file = self.processing_pipeline.preprocess(loaded_cadd_data=imputed_file, train=True)
        self.assertIsNone(preprocessor.get_model_features())


if __name__ == '__main__':
    unittest.main()
