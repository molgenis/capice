import numpy as np
import pandas as pd

from molgenis.capice.vep.template import Template


class Consequence(Template):
    def __init__(self):
        super(Consequence, self).__init__(
            name='Consequence',
            usable=True
        )

    @property
    def drop(self):
        return True

    @property
    def columns(self):
        return ['is_regulatory_region_variant',
                'is_regulatory_region_ablation',
                'is_regulatory_region_amplification',
                'is_missense_variant',
                'is_intron_variant',
                'is_upstream_gene_variant',
                'is_downstream_gene_variant',
                'is_synonymous_variant',
                'is_TF_binding_site_variant',
                'is_splice_donor_variant',
                'is_coding_sequence_variant',
                'is_splice_region_variant',
                'is_stop_gained',
                'is_splice_acceptor_variant',
                'is_frameshift_variant',
                'is_3_prime_UTR_variant',
                'is_inframe_insertion',
                'is_inframe_deletion',
                'is_5_prime_UTR_variant',
                'is_start_lost',
                'is_non_coding_transcript_exon_variant',
                'is_non_coding_transcript_variant',
                'is_TFBS_ablation',
                'is_TFBS_amplification',
                'is_protein_altering_variant',
                'is_stop_lost',
                'is_stop_retained_variant',
                'is_transcript_ablation',
                'is_intergenic_variant',
                'is_start_retained_variant',
                'is_transcript_amplification',
                'is_incomplete_terminal_codon_variant',
                'is_mature_miRNA_variant',
                'is_NMD_transcript_variant',
                'is_feature_elongation',
                'is_feature_truncation']

    def _process(self, dataframe: pd.DataFrame):
        splitted_consequence = dataframe[self.name].str.split('&', expand=True)
        for consequence in self.columns:
            current_consequence = consequence.split('is_')[1]
            dataframe[consequence] = np.where(
                np.isin(splitted_consequence, current_consequence).any(axis=1), 1, 0
            )
        return dataframe
