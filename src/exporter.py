from src.utilities.utilities import check_file_exists
from src.global_manager import CapiceManager
from src.logger import Logger
import os
import pandas as pd


class Exporter:
    def __init__(self, file_path):
        self.log = Logger().get_logger()
        self.force = CapiceManager().get_force()
        self.now = CapiceManager().get_now()
        self.file_path = file_path
        self.file_name = 'capice_{}'.format(self.now.strftime("%H%M%S%f_%d%m%Y"))
        self.export_cols = ['chr_pos_ref_alt', 'ID', 'GeneName', 'FeatureID', 'Consequence', 'probabilities']

    def export(self, datafile: pd.DataFrame):
        filename = self._export_filename_ready()
        datafile[self.export_cols].to_csv(filename, sep='\t', index=False)
        self.log.info('Successfully exported CAPICE datafile to: {}'.format(filename))

    def _export_filename_ready(self):
        path_and_filename = os.path.join(self.file_path, self.file_name)
        extension = '.tsv'
        full_path = os.path.join(self.file_path, self.file_name + extension)
        export_path = None
        if not check_file_exists(full_path):
            self.log.info('No file found at {}, save to create.'.format(full_path))
            export_path = full_path
        elif self.force and check_file_exists(full_path):
            self.log.info('Found existing file at {}, removing file for overwriting.'.format(full_path))
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
