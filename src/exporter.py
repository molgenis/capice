from src.utilities.utilities import check_file_exists
from src.global_manager import CapiceManager
from src.logger import Logger
import os
import pandas as pd
import pickle


class Exporter:
    def __init__(self, file_path):
        self.log = Logger().get_logger()
        self.force = CapiceManager().get_force()
        self.now = CapiceManager().get_now()
        self.file_path = file_path
        self.export_cols = ['chr_pos_ref_alt', 'ID', 'GeneName', 'FeatureID', 'Consequence', 'probabilities']

    def export_capice_prediction(self, datafile: pd.DataFrame):
        file_name_capice = 'capice_{}'.format(self.now.strftime("%H%M%S%f_%d%m%Y"))
        filename = self._export_filename_ready(file_name=file_name_capice)
        datafile[self.export_cols].to_csv(filename, sep='\t', index=False)
        self.log.info('Successfully exported CAPICE datafile to: {}'.format(filename))

    def export_capice_training_dataset(self, datafile: pd.DataFrame, name: str, feature: str):
        filename = self._export_filename_ready(file_name=name, type_export='dataset')
        datafile.to_csv(filename, sep='\t', compression='gzip', index=False)
        self.log.info('Exported {} with shape {} to: {}'.format(feature, datafile.shape, filename))

    def export_capice_model(self, model, model_type):
        export_name = ""
        if model_type == "XGBClassifier":
            export_name = 'xgb_classifier'
        elif model_type == 'RandomizedSearchCV':
            export_name = 'randomized_search_cv'
        filename_model = '{}_{}'.format(export_name, self.now.strftime("%H%M%S%f_%d%m%Y"))
        filename = self._export_filename_ready(file_name=filename_model, type_export='model')
        pickle.dump(model, open(filename, 'wb'))

    def _export_filename_ready(self, file_name, type_export='prediction'):
        path_and_filename = os.path.join(self.file_path, file_name)
        types_export_and_extensions = {'prediction': '.tsv',
                                       'dataset': '.tsv.gz',
                                       'model': '.pickle.dat'}
        extension = types_export_and_extensions[type_export]
        full_path = os.path.join(self.file_path, file_name + extension)
        export_path = None
        if not check_file_exists(full_path):
            self.log.info('No file found at {}, save to create.'.format(full_path))
            export_path = full_path
        elif self.force and check_file_exists(full_path):
            self.log.warning('Found existing file at {}, removing file for overwriting.'.format(full_path))
            os.remove(full_path)
            export_path = full_path
        else:
            self.log.info('Found existing file at {}, not able to overwrite. Creating new filename.'.format(
                full_path
            ))
            export_exists = True
            extension_counter = 1
            while export_exists:
                attempted_file = path_and_filename + "_{}".format(extension_counter) + extension
                if not check_file_exists(attempted_file):
                    self.log.info('Able to create {}'.format(attempted_file))
                    export_exists = False
                    export_path = attempted_file
                extension_counter += 1
        return export_path
