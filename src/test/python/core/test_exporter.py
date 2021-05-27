import os
import unittest
import pandas as pd
from src.test.python.test_templates import set_up_manager_and_loc, teardown
from src.main.python.core.exporter import Exporter
from src.main.python.resources.enums.sections import Column


class TestExporter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_loc = set_up_manager_and_loc()
        cls.exporter = Exporter(file_path=cls.output_loc)
        cls.prediction_output_dataframe = pd.DataFrame({
            Column.chr_pos_ref_alt.value: ['1_100_A_C', '2_200_T_G'],
            Column.GeneName.value: ['foo', 'bar'],
            Column.FeatureID.value: ['TRANS_01', 'TRANS_02'],
            Column.Consequence.value: ['Synonymous', 'Frame-shift'],
            Column.probabilities.value: [0.01, 0.998]
        })
        cls.legacy_export_prediction = pd.DataFrame(
            {
                Column.chr_pos_ref_alt.value: ['1_100_A_C', '2_200_T_G'],
                Column.GeneName.value: ['foo', 'bar'],
                Column.Consequence.value: ['Synonymous', 'Frame-shift'],
                Column.PHRED.value: [0.0, 0.0],
                Column.probabilities.value: [0.01, 0.998],
                Column.prediction.value: ['empty', 'empty'],
                Column.combined_prediction.value: ['empty', 'empty']
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
        self.exporter.capice_filename = 'test_output.tsv'
        self.exporter.export_capice_prediction(datafile=self.prediction_output_dataframe)
        exported_data = pd.read_csv(os.path.join(self.output_loc, 'test_output.tsv'), sep='\t')
        pd.testing.assert_frame_equal(exported_data, self.legacy_export_prediction)

    def test_legacy_conversion(self):
        print('Legacy output conversion')
        converted_legacy = self.exporter._export_legacy_prediction(datafile=self.prediction_output_dataframe)
        pd.testing.assert_frame_equal(converted_legacy, self.legacy_export_prediction)

    def test_dataset_export(self):
        print('Dataset export')
        self.exporter.export_capice_training_dataset(
            datafile=self.export_dataset,
            name='test',
            feature='Testing dataset'
        )
        exported_dataset = pd.read_csv(os.path.join(self.output_loc, 'test.tsv.gz'), sep='\t')
        pd.testing.assert_frame_equal(exported_dataset, self.export_dataset)

    def test_exporter_filename_generator_dataset_extension(self):
        print('Filename generator (with dataset and extension=True)')
        with open(os.path.join(self.output_loc, 'filename.tsv.gz'), 'wt') as fake_file:
            fake_file.write('This is a fake file')
        new_filename = self.exporter._export_filename_ready(file_name='filename')
        self.assertEqual(new_filename, os.path.join(self.output_loc, 'filename_1.tsv.gz'))

    def test_exporter_force(self):
        print('Filename generator (with force=True)')
        with open(os.path.join(self.output_loc, 'already_present_file.tsv'), 'wt') as present_file:
            present_file.write('This file is already present')
        self.exporter.force = True
        self.exporter.capice_filename = 'already_present_file.tsv'
        self.exporter.export_capice_prediction(datafile=self.prediction_output_dataframe)
        forced_file = pd.read_csv(os.path.join(self.output_loc, 'already_present_file.tsv'), sep='\t')
        pd.testing.assert_frame_equal(forced_file, self.legacy_export_prediction)


if __name__ == '__main__':
    unittest.main()
