from src.main.python.resources.utilities.utilities import  \
    get_filename_and_extension
from src.main.python.resources.enums.sections import Column
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.logger import Logger
import os
import pandas as pd
import pickle


class Exporter:
    """
    Class specifically export files and create unique filenames.
    """

    def __init__(self, file_path):
        self.log = Logger().logger
        self.now = CapiceManager().now
        self.capice_filename = CapiceManager().output_filename
        self.file_path = file_path
        self.export_cols = [Column.chr.value,
                            Column.pos.value,
                            Column.ref.value,
                            Column.alt.value,
                            Column.gene_name.value,
                            Column.gene_id.value,
                            Column.id_source.value,
                            Column.transcript.value,
                            Column.score.value]

    def export_capice_prediction(self, datafile: pd.DataFrame):
        """
        Function specific to export the dataset created for the prediction
        pathway.
        :param datafile: prediction pandas DataFrame
        """
        export_loc = os.path.join(self.file_path, self.capice_filename)
        datafile = self._post_process_split_cols(datafile)
        datafile = self._post_process_set_correct_dtypes(datafile)
        datafile[self.export_cols].to_csv(
            export_loc,
            sep='\t',
            compression='gzip',
            index=False
        )
        self.log.info(
            'Successfully exported CAPICE datafile to: %s', export_loc
        )

    @staticmethod
    def _post_process_split_cols(datafile: pd.DataFrame):
        datafile[
            [Column.chr.value,
             Column.pos.value,
             Column.ref.value,
             Column.alt.value
             ]
        ] = datafile[Column.chr_pos_ref_alt.value].str.split(
            '_',
            expand=True
        )
        return datafile

    @staticmethod
    def _post_process_set_correct_dtypes(datafile: pd.DataFrame):
        datafile[Column.gene_id.value] = pd.Series(
            datafile[Column.gene_id.value],
            dtype='Int64'
        )
        return datafile

    def export_capice_training_dataset(self, datafile: pd.DataFrame, name: str,
                                       feature: str):
        """
        Function specific to export a (splitted) dataset comming from the
        training pathway.
        :param datafile: pandas DataFrame
        :param name: Name of the export file
        :param feature: Name of what is exported
        """
        filename = self._export_filename_ready(file_name=name)
        datafile.to_csv(filename, sep='\t', compression='gzip', index=False)
        self.log.info(
            'Exported %s with shape %s to: %s',
            feature,
            datafile.shape,
            filename
        )

    def export_capice_model(self, model, model_type):
        """
        Function specific to export a newly created CAPICE model
        :param model: RandomizedSearchCV or XGBClassifier instance
        :param model_type: either "XGBClassifier" or "RandomizedSearchCV"
        """
        export_name = ""
        if model_type == 'XGBClassifier':
            export_name = 'xgb_classifier'
        elif model_type == 'RandomizedSearchCV':
            export_name = 'randomized_search_cv'
        filename_model = '{}_{}'.format(
            export_name, self.now.strftime("%H%M%S%f_%d%m%Y")
        )
        filename = self._export_filename_ready(
            file_name=filename_model,
            type_export='model'
        )
        with open(filename, 'wb') as model_dump:
            pickle.dump(model, model_dump)

    def _export_filename_ready(self, file_name, type_export='dataset',
                               check_extension=True):
        """
        Function to build an unique filename in case that force is turned off.
        :param file_name: Name of the to be created file
        :param type_export: "prediction" for the prediction pathway,
            "dataset" for the export of datasets or
            "model" for the export of models.
        :param check_extension: Boolean if the extension should be
        checked before exporting.
        :return: full export path
        """
        path_and_filename = os.path.join(self.file_path, file_name)
        types_export_and_extensions = {'dataset': '.tsv.gz',
                                       'model': '.pickle.dat'}
        if check_extension:
            extension = types_export_and_extensions[type_export]
            if not file_name.endswith(extension):
                file_name = file_name + extension
        full_path = os.path.join(self.file_path, file_name)
        export_path = None
        if not os.path.exists(full_path):
            self.log.info(
                'No file found at %s, save to create.', full_path)
            export_path = full_path
        elif self.force and os.path.exists(full_path):
            self.log.warning(
                'Found existing file at %s, removing file for overwriting.',
                full_path
            )
            os.remove(full_path)
            export_path = full_path
        else:
            self.log.info(
                'Found existing file at %s, not able to overwrite. '
                'Creating new filename.',
                full_path
            )
            filename, extension = get_filename_and_extension(full_path)
            basedir = os.path.dirname(path_and_filename)
            export_exists = True
            extension_counter = 1
            while export_exists:
                attempted_file = os.path.join(
                    basedir,
                    filename + "_{}.".format(extension_counter) + extension
                )
                if not os.path.isfile(attempted_file):
                    self.log.info('Able to create %s', attempted_file)
                    export_exists = False
                    export_path = attempted_file
                extension_counter += 1
        return export_path
