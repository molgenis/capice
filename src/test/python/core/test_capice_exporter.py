import os
import unittest
import numpy as np
import pandas as pd

from src.main.python.core.capice_exporter import CapiceExporter
from src.main.python.utilities.enums import Column
from src.test.python.test_templates import set_up_manager_and_out, teardown


class TestCapiceExporter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_path = set_up_manager_and_out()
        cls.exporter = CapiceExporter(file_path=cls.output_path)
        cls.prediction_output_dataframe = pd.DataFrame(
            {
                Column.chr_pos_ref_alt.value: [
                    '1_VeryUniqueCAPICESeparator_100'
                    '_VeryUniqueCAPICESeparator_A_VeryUniqueCAPICESeparator_C',
                    '2_VeryUniqueCAPICESeparator_200'
                    '_VeryUniqueCAPICESeparator_T_VeryUniqueCAPICESeparator_G'
                ],
                Column.gene_name.value: ['foo', 'bar'],
                Column.gene_id.value: [1000, 2000],
                Column.id_source.value: ['foo', 'bar'],
                Column.transcript.value: ['TRANS_01', 'TRANS_02'],
                Column.score.value: [0.01, 0.998]
            }
        )
        cls.expected_prediction_output_dataframe = pd.DataFrame(
            {
                Column.chr.value: ['1', '2'],
                Column.pos.value: [100, 200],
                Column.ref.value: ['A', 'T'],
                Column.alt.value: ['C', 'G'],
                Column.gene_name.value: ['foo', 'bar'],
                Column.gene_id.value: [1000, 2000],
                Column.id_source.value: ['foo', 'bar'],
                Column.transcript.value: ['TRANS_01', 'TRANS_02'],
                Column.score.value: [0.01, 0.998]
            }
        )
        cls.export_dataset = pd.DataFrame(
            {
                'chr': [1, 2],
                'pos': [100, 200],
                'ref': ['A', 'A'],
                'alt': ['C', 'G'],
                'feature_1': [0.001, 0.2],
                'feature_2': [0.02, 5.5]
            }
        )

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def setUp(self):
        print('Testing case:')

    def test_prediction_output(self):
        print('Prediction output')
        filename = 'test_output.tsv'
        filename_path = os.path.join(self.output_path, filename)
        self.exporter.capice_filename = filename
        self.exporter.export_capice_prediction(datafile=self.prediction_output_dataframe)
        self.assertTrue(os.path.isfile(filename_path))
        exported_data = pd.read_csv(filename_path, compression='gzip', sep='\t')
        exported_data[Column.chr.value] = exported_data[Column.chr.value].astype(str)
        pd.testing.assert_frame_equal(exported_data, self.expected_prediction_output_dataframe)

    def test_exporter_force(self):
        """
        Since force is dealt with at the very start of CAPICE and raises an
        error if the output file is already present unless the force flag is
        True, this test just makes sure that the overwritten file is correct.
        """
        print('Filename generator (with force=True)')
        present_file = 'already_present_file.tsv'
        present_file_path = os.path.join(self.output_path, present_file)
        with open(present_file_path, 'wt') as present_file_conn:
            present_file_conn.write('This file is already present')
        self.exporter.capice_filename = present_file
        self.exporter.export_capice_prediction(datafile=self.prediction_output_dataframe)
        forced_file = pd.read_csv(present_file_path, compression='gzip', sep='\t')
        forced_file[Column.chr.value] = forced_file[Column.chr.value].astype(str)
        pd.testing.assert_frame_equal(forced_file, self.expected_prediction_output_dataframe)

    def test_post_process_set_correct_dtypes(self):
        print('Test post process set correct dtypes')
        some_data = pd.DataFrame(
            {
                'foo': [1, 2, 3],
                Column.gene_id.value: [1, np.nan, 3]
            }
        )
        expected_output = some_data.copy(deep=True)
        expected_output[Column.gene_id.value] = pd.Series(
            expected_output[Column.gene_id.value], dtype='Int64'
        )
        out_data = self.exporter._post_process_set_correct_dtypes(some_data)
        pd.testing.assert_frame_equal(
            out_data.sort_index(axis=1),
            expected_output.sort_index(axis=1)
        )


if __name__ == '__main__':
    unittest.main()
