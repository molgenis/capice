import json
import os
import unittest

import pandas as pd

from molgenis.capice.main_train import CapiceTrain
from tests.capice.test_templates import set_up_manager_and_out, teardown, _project_root_directory, \
    load_model


class TestMainTrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        manager, cls.output_dir = set_up_manager_and_out()
        cls.output_filename = 'train_example_capice.pickle.dat'
        manager.output_filename = cls.output_filename

    @classmethod
    def tearDownClass(cls):
        print('Performing teardown.')
        teardown()

    def tearDown(self):
        print('Resetting arguments.')

    def setUp(self):
        print('Performing test:')
        train_file = os.path.join(_project_root_directory, 'resources', 'train_input.tsv.gz')
        impute_json = os.path.join(_project_root_directory,
                                   'resources',
                                   'train_features.json')
        self.main = CapiceTrain(input_path=train_file,
                                json_path=impute_json,
                                test_split=0.2,
                                output_path=self.output_dir,
                                threads=2,
                                output_given=True)
        self.main.esr = 1
        self.main.n_jobs = 2
        self.main.cross_validate = 2
        self.main.n_iterations = 2

    def test_validate_train_features_duplicates_fail(self):
        test_features = ['foo', 'bar', 'baz', 'foo']
        with self.assertRaises(KeyError) as e:
            self.main._validate_train_features_duplicates(test_features)
        # Double quotes since KeyError still adds single quotes to the error.exception
        self.assertEqual(
            "'Detected duplicate features in user supplied train features: foo'",
            str(e.exception)
        )

    def test_validate_train_features_duplicates_pass(self):
        test_features = ['foo', 'bar', 'baz']
        self.main._validate_train_features_duplicates(test_features)

    def test_component_reset_train_features(self):
        user_input = ['REF', 'Amino_acids', 'foo']
        vep_processed = {
            'REF': ['Type', 'Length'],
            'Amino_acids': ['oAA', 'nAA']
        }
        dataset = pd.DataFrame(
            columns=['REF', 'oAA', 'nAA', 'foo']
        )
        observed = self.main._reset_processing_features(
            user_input, vep_processed, dataset.columns)
        # Set because order is not important
        self.assertSetEqual(set(observed), {'REF', 'oAA', 'nAA', 'foo', 'Type', 'Length'})

    def test_integration_reset_train_features(self):
        with open(self.main.json_path, 'rt') as fh:
            user_input = list(json.load(fh).keys())
        self.main._validate_train_features_duplicates(user_input)
        data = self.main._load_file(additional_required_features=self.main.additional_required)
        self.main._validate_features_present(data, user_input)
        data_processed, vep_processed = self.main.process(data, user_input)
        observed = self.main._reset_processing_features(
            user_input, vep_processed, data_processed.columns
        )
        expected = [
            'PolyPhenCat', 'PolyPhenVal', 'cDNApos', 'relcDNApos', 'SIFTcat', 'SIFTval',
            'protPos', 'relProtPos', 'oAA', 'nAA', 'CDSpos', 'relCDSpos', 'REF', 'ALT',
            'is_regulatory_region_variant', 'is_regulatory_region_ablation',
            'is_regulatory_region_amplification', 'is_missense_variant', 'is_intron_variant',
            'is_upstream_gene_variant', 'is_downstream_gene_variant', 'is_synonymous_variant',
            'is_TF_binding_site_variant', 'is_splice_donor_variant', 'is_coding_sequence_variant',
            'is_splice_region_variant', 'is_stop_gained', 'is_splice_acceptor_variant',
            'is_splice_donor_5th_base_variant', 'is_splice_donor_region_variant',
            'is_splice_polypyrimidine_tract_variant', 'is_frameshift_variant',
            'is_3_prime_UTR_variant', 'is_inframe_insertion',
            'is_inframe_deletion', 'is_5_prime_UTR_variant', 'is_start_lost',
            'is_non_coding_transcript_exon_variant', 'is_non_coding_transcript_variant',
            'is_TFBS_ablation', 'is_TFBS_amplification', 'is_protein_altering_variant',
            'is_stop_lost', 'is_stop_retained_variant', 'is_transcript_ablation',
            'is_intergenic_variant', 'is_start_retained_variant', 'is_transcript_amplification',
            'is_incomplete_terminal_codon_variant', 'is_mature_miRNA_variant',
            'is_NMD_transcript_variant', 'is_feature_elongation', 'is_feature_truncation',
            'SpliceAI_pred_DP_AG', 'SpliceAI_pred_DP_AL', 'SpliceAI_pred_DP_DG',
            'SpliceAI_pred_DP_DL', 'SpliceAI_pred_DS_AG', 'SpliceAI_pred_DS_AL',
            'SpliceAI_pred_DS_DG', 'SpliceAI_pred_DS_DL', 'Type', 'Length', 'Grantham', 'phyloP']
        self.assertSetEqual(set(observed), set(expected))

    def test_integration_training(self):
        """
        Integration test for the full training part of CAPICE.
        With check if the correct class is exported.
        """
        print('Training (integration)')
        self.main.run()
        output_path = os.path.join(self.output_dir, self.output_filename)
        model = load_model(output_path)
        best_model = str(model.__class__).split("'")[1]
        self.assertEqual('xgboost.sklearn.XGBClassifier', best_model)

    def test_params(self):
        """
        Test to see if the >1.6.2 XGBoost parameter settings are applied correctly to the model
        """
        print('Test params')
        self.main.run()
        output_path = os.path.join(self.output_dir, self.output_filename)
        model = load_model(output_path)
        self.assertEqual(model.get_params()['early_stopping_rounds'], 1)
        self.assertEqual(model.get_params()['eval_metric'], ['auc'])

    def test_unit_split(self):
        """
        Unit test to see if split works.
        """
        print('Split (unit)')
        input_file = self.main._load_file()
        self.main.split_data(dataset=input_file, test_size=0.2)

    def test_component_split(self):
        """
        Component test for split to see if the correct sizes of datasets are
        created.
        """
        print('Split (component)')
        input_file = self.main._load_file()
        train, test = self.main.split_data(dataset=input_file, test_size=0.2)
        total_size = input_file.shape[0]
        self.assertAlmostEqual(train.shape[0], total_size * 0.8, delta=1)
        self.assertAlmostEqual(test.shape[0], total_size * 0.2, delta=1)
        self.assertEqual(train.shape[0] + test.shape[0], total_size)

    def test__set_verbosity_from_log_level_none(self):
        """
        Component test for _set_verbosity_from_log_level when there is no log level set.
        Expects verbosity set to 0 and false.
        """
        verbosity, xgb_verbosity = self.main._set_verbosity_from_log_level()
        self.assertFalse(verbosity)
        self.assertEqual(0, xgb_verbosity)

    def test__set_verbosity_from_log_level_10(self):
        """
        Component test for _set_verbosity_from_log_level with log level 10
        Expects verbosity to be set to 1 and true.
        """
        self.main.loglevel = 10
        verbosity, xgb_verbosity = self.main._set_verbosity_from_log_level()
        self.assertTrue(verbosity)
        self.assertEqual(1, xgb_verbosity)

    def test__set_eval_set_test(self):
        """
        Component test for _create_eval_set for test version of xg boost
        Should return list with tuple with:
            a dataframe with the processed features,
            a dataseries of binarized label
            "test"
        """
        processed_features = ['feat1', 'feat2']
        self.main.train_features = processed_features
        test_set = pd.DataFrame(data={
            'binarized_label': [0, 1, 0],
            'feat1': [1, 0, 0],
            'feat2': [1, 0, 1],
            'feat3': [0, 0, 0],
            'test': [1, 1, 1]
        })
        eval_set = self.main._create_eval_set('0.0.1', test_set)
        pd.testing.assert_frame_equal(test_set[['feat1', 'feat2']], eval_set[0][0])
        pd.testing.assert_series_equal(test_set['binarized_label'], eval_set[0][1])
        self.assertEqual('test', eval_set[0][2])

    def test__set_eval_set(self):
        """
        Component test for _create_eval_set for test version of xg boost
        Should return list with tuple with:
            a dataframe with the processed features,
            a dataseries of binarized label
            (length should be 2, as "test" shouldn't be included)
        """
        processed_features = ['feat1', 'feat2']
        self.main.train_features = processed_features
        test_set = pd.DataFrame(data={
            'binarized_label': [0, 1, 0],
            'feat1': [1, 0, 0],
            'feat2': [1, 0, 1],
            'feat3': [0, 0, 0],
            'test': [1, 1, 1]
        })
        eval_set = self.main._create_eval_set('1.0.1', test_set)
        pd.testing.assert_frame_equal(test_set[['feat1', 'feat2']], eval_set[0][0])
        pd.testing.assert_series_equal(test_set['binarized_label'], eval_set[0][1])
        self.assertEqual(2, len(eval_set[0]))

    def test_full_processed_features(self):
        loaded_dataset = pd.DataFrame(
            {
                'REF': ['C', 'GC'],
                'ALT': ['A', 'G'],
                'PolyPhen': [0.1, 0.01],
                'SIFT': [0.1, 0.01],
                'Other_feature': ['foo', 'bar']
            }
        )
        features = ['REF', 'ALT', 'PolyPhen', 'SIFT']
        processed_data, vep_processed = self.main.process(loaded_dataset, features)
        resetted_features = self.main._reset_processing_features(
            features, vep_processed, processed_data.columns)
        self.assertSetEqual(
            {'REF', 'ALT', 'Length', 'Type', 'PolyPhenVal', 'PolyPhenCat', 'SIFTval', 'SIFTcat'},
            set(resetted_features)
        )

    def test_component_feature_selection(self):
        test_case = pd.DataFrame(
            {
                'chr': [1, 2, 3],
                'pos': [1, 2, 3],
                'REF': ['A', 'AT', 'ATCG'],
                'ALT': ['C', 'G', 'ATGCAB'],
                'REFSEQ_MATCH': ['foo', 'bar', 'baz'],  # Included because of REF, can cause issues
                'ALTERNATIVE_FEATURE': ['foo', 'bar', 'baz'],
                'feature_1': ['foo_bar', 'bar', 'baz']
            }
        )
        user_input = ['REF', 'ALT', 'Type', 'Length', 'feature_1']
        processed_data, vep_processed = self.main.process(test_case, user_input)
        self.assertIn(
            'REF',
            vep_processed
        )
        self.assertSetEqual(
            set(vep_processed['REF']),
            {'Type', 'Length'}
        )
        processable_features = self.main._reset_processing_features(
            user_input, vep_processed, processed_data.columns
        )
        self.assertSetEqual(
            set(processable_features),
            {'REF', 'ALT', 'Type', 'Length', 'feature_1'}
        )
        fully_processed_data, processed_features = self.main.categorical_process(
            processed_data, train_features=processable_features, processing_features=None
        )
        # Test to see if REF is successfully processed
        self.assertIn(
            'REF_A',
            fully_processed_data.columns
        )
        # Test to see if REFSEQ is successfully skipped
        self.assertNotIn(
            'REFSEQ_MATCH_foo',
            fully_processed_data.columns
        )
        # Another test to see if feature_1 is successfully processed
        self.assertIn(
            'feature_1_foo_bar',
            fully_processed_data.columns
        )
        # Test to see if category A is successfully saved for REF
        self.assertIn(
            'A',
            processed_features['REF']
        )

        self.main._set_train_features(
            processable_features, processed_features
        )

        # Test to see if REF_A is successfully inserted into the final training features
        self.assertIn(
            'REF_A',
            self.main.train_features
        )

        # Test to see if REFSEQ_MATCH_foo is successfully skipped
        self.assertNotIn(
            'REFSEQ_MATCH_foo',
            self.main.train_features
        )
        # Test to see if multiple underscores also get successfully inserted
        self.assertIn(
            'feature_1_foo_bar',
            self.main.train_features
        )
        self.assertSetEqual(
            set(self.main.train_features),
            {
                'REF_A', 'REF_AT', 'REF_ATCG',
                'ALT_C', 'ALT_G', 'ALT_ATGCAB',
                'Type_DELINS', 'Type_SNV',
                'Length',
                'feature_1_foo_bar', 'feature_1_bar', 'feature_1_baz'
            }
        )


if __name__ == '__main__':
    unittest.main()
