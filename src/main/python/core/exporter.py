import os
import pickle
import pandas as pd
from src.main.python.core.logger import Logger
from src.main.python.resources.enums.sections import Column
from src.main.python.core.global_manager import CapiceManager


class Exporter:
    """
    Class specifically exporting files
    """

    def __init__(self, file_path):
        self.log = Logger().logger
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

    def export_capice_model(self, model):
        """
        Function specific to export a newly created CAPICE model
        :param model: XGBClassifier instance
        """
        export_loc = os.path.join(self.file_path, self.capice_filename)
        with open(export_loc, 'wb') as model_dump:
            pickle.dump(model, model_dump)
