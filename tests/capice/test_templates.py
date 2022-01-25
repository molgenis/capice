import os
import pickle
from pathlib import Path

from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.core.logger import Logger
from molgenis.capice.main_predict import CapicePredict

_project_root_directory = Path(__file__).absolute().parent.parent.parent


def set_up_manager_and_out():
    """
    Function to set up the CapiceManager and testing output location
    :return: manager instance, output_directory
    """
    manager = CapiceManager()
    manager.critical_logging_only = True
    root_dir = _project_root_directory
    output_directory = os.path.join(root_dir, '.test_output')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return manager, output_directory


def teardown():
    """
    Function to remove any and all files from the '.test_output' folder and
    remove the folder itself too.
    """
    test_folder = os.path.join(_project_root_directory, '.test_output')
    if os.path.isdir(test_folder):
        if len(os.listdir(test_folder)) > 0:
            for file in os.listdir(test_folder):
                os.remove(os.path.join(test_folder, file))
        os.rmdir(test_folder)
    Logger.instance = None
    CapiceManager.instance = None


def set_up_predict():
    return CapicePredict(input_path=None, model=None, output_path=None)


def set_up_impute_preprocess():
    set_up_manager_and_out()
    main = set_up_predict()
    main.infile = os.path.join(_project_root_directory, 'CAPICE_example', 'CAPICE_input.tsv.gz')
    with open(
            os.path.join(
                _project_root_directory,
                'tests',
                'resources',
                'xgb_booster_poc.pickle.dat'
            ), 'rb'
    ) as model_file:
        model = pickle.load(model_file)
    main.model = model
    return main, model
