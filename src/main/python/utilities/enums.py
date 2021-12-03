from enum import Enum


class Column(Enum):
    """
    Enums to use that are specific to the column names after .
    """
    chr_pos_ref_alt = 'chr_pos_ref_alt'
    chr = 'chr'
    pos = 'pos'
    ref = 'ref'
    alt = 'alt'
    gene_name = 'gene_name'
    gene_id = 'gene_id'
    id_source = 'id_source'
    transcript = 'transcript'
    score = 'score'


class TrainEnums(Enum):
    """
    Enums to use within the training module of CAPICE.
    """
    Consequence = 'Consequence'
    max_AF = 'max_AF'
    sample_weight = 'sample_weight'
    binarized_label = 'binarized_label'
    learning_rate = 'learning_rate'
    max_depth = 'max_depth'
    n_estimators = 'n_estimators'


class Domains(Enum):
    """
    Enums specific to the VEP processor that does the processing for Domains.
    """
    ncoils = 0
    signalp = 1
    lowcomplex = 2
    ndomain = 3
    panther = 4
    other = 5


class UniqueSeparator(Enum):
    """
    Enum specific to creating a specific separator for the preservation of the chr pos ref alt
    columns.
    """
    unique_separator = '_VeryUniqueCAPICESeparator_'
