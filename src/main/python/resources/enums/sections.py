from enum import Enum


class Sections(Enum):
    DEFAULTS = 'DEFAULTS'
    OVERWRITES = 'OVERWRITES'
    MISC = 'MISC'
    DATAFILES = 'DATAFILES'
    TRAINING = 'TRAINING'


class Column(Enum):
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


class Train(Enum):
    Consequence = Column.Consequence.value
    max_AF = 'max_AF'
    sample_weight = 'sample_weight'
    binarized_label = 'binarized_label'
    learning_rate = 'learning_rate'
    max_depth = 'max_depth'
    n_estimators = 'n_estimators'
