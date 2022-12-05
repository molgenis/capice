import os
from enum import Enum
from pathlib import Path

from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.core.logger import Logger
from molgenis.capice.main_predict import CapicePredict

_project_root_directory = Path(__file__).absolute().parent.parent.parent
_project_resources = os.path.join(_project_root_directory, 'resources')
_project_test_resources = os.path.join(_project_root_directory, 'tests/resources')


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
    return CapicePredict(input_path=None, model=None, output_path=None, output_given=False)


def set_up_impute_preprocess():
    set_up_manager_and_out()
    main = set_up_predict()
    main.infile = os.path.join(_project_root_directory, 'resources', 'predict_input.tsv.gz')
    model = ArgsHandlerParent.load_model(ResourceFile.XGB_BOOSTER_POC_UBJ.value)
    main.model = model
    return main, model


def load_model(file_path):
    return ArgsHandlerParent.load_model(file_path)


class ResourceFile(Enum):
    """
    Enum storing paths to test resource files for easy access.
    """
    PREDICT_INPUT_TSV_GZ = os.path.join(_project_resources, 'predict_input.tsv.gz')
    XGB_BOOSTER_POC_UBJ = os.path.join(_project_test_resources, 'xgb_booster_poc.ubj')


class FakeResourceFile(Enum):
    PREDICT_INPUT_TSV_GZ = os.path.join(_project_test_resources,
                                        'non_existing_predict_input.tsv.gz')
