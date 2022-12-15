import os

import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.utilities.enums import Column, UniqueSeparator


class CapiceExporter:
    """
    Class specifically exporting files
    """

    def __init__(self, file_path, output_given):
        self.log = Logger().logger
        self.capice_filename = CapiceManager().output_filename
        self.file_path = file_path
        self.output_given = output_given
        self.export_cols = [
            Column.chr.value,
            Column.pos.value,
            Column.ref.value,
            Column.alt.value,
            Column.gene_name.value,
            Column.gene_id.value,
            Column.id_source.value,
            Column.feature.value,
            Column.feature_type.value,
            Column.score.value,
            Column.suggested_class.value
        ]

    def export_capice_prediction(self, datafile: pd.DataFrame):
        """
        Function specific to export the dataset created for the prediction
        pathway.
        :param datafile: prediction pandas DataFrame
        """
        export_path = os.path.join(self.file_path, self.capice_filename)
        datafile = self._post_process_split_cols(datafile)
        datafile = self._post_process_set_correct_dtypes(datafile)
        datafile[self.export_cols].to_csv(export_path, sep='\t', index=False)
        if not self.output_given:
            print('Successfully exported CAPICE datafile to: %s', export_path)

    @staticmethod
    def _post_process_split_cols(datafile: pd.DataFrame):
        datafile[
            [Column.chr.value, Column.pos.value, Column.ref.value, Column.alt.value]
        ] = datafile[Column.chr_pos_ref_alt.value].str.split(
            UniqueSeparator.unique_separator.value, expand=True)
        return datafile

    @staticmethod
    def _post_process_set_correct_dtypes(datafile: pd.DataFrame):
        datafile[Column.gene_id.value] = pd.Series(datafile[Column.gene_id.value], dtype='Int64')
        return datafile

    def export_capice_model(self, model):
        """
        Function specific to export a newly created CAPICE model
        :param model: XGBClassifier instance
        """
        export_path = os.path.join(self.file_path, self.capice_filename)
        model.save_model(export_path)
        if not self.output_given:
            print('Successfully exported CAPICE model to: ', export_path)
