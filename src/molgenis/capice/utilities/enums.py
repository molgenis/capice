from enum import Enum


class InputColumn(Enum):
    """
    Columns within panda data frames.
    `col_name` is the column name as should be used within CAPICE after processing input & the
    column name in the output file.
    `col_input_name` is the expected name as given by the input file.

    If `col_name` and `col_input_name` are equal, the name does not get altered.

    The `dtype` contains the type as which it needs to be loaded within pandas. If a manual
    processor needs to adjust the column still, use `object`. Otherwise, state the correct type
    (string/int64/etc.)
    """
    # General
    chr = ('chr', 'CHROM', 'string')
    pos = ('pos', 'POS', 'int64')
    ref = ('REF', 'REF', 'category')
    alt = ('ALT', 'ALT', 'category')
    gene_name = ('gene_name', 'SYMBOL', 'string')
    gene_id = ('gene_id', 'Gene', 'Int64')
    id_source = ('id_source', 'SYMBOL_SOURCE', 'string')
    feature = ('feature', 'Feature', 'string')
    feature_type = ('feature_type', 'Feature_type', 'string')

    # Train-only
    binarized_label = ('binarized_label', 'binarized_label', 'float64')
    sample_weight = ('sample_weight', 'sample_weight', 'float64')

    def __init__(self, col_name, col_input_name, dtype):
        self.col_name = col_name
        self.col_input_name = col_input_name
        self.dtype = dtype

    @staticmethod
    def get_input_name_dtype_dict():
        input_name_dtype = {}
        for col in InputColumn:
            input_name_dtype[col.col_input_name] = col.dtype
        return input_name_dtype


class PredictOutputColumn(Enum):
    score = 'score'
    suggested_class = 'suggested_class'
    other = 'other_CAPICE_value'


class Column(Enum):
    """
    Enums to use that are specific to the column names after.
    """
    chr_pos_ref_alt = 'chr_pos_ref_alt'
    chr = 'chr'
    pos = 'pos'
    ref = 'REF'
    alt = 'ALT'
    gene_name = 'gene_name'
    gene_id = 'gene_id'
    id_source = 'id_source'
    feature = 'feature'
    feature_type = 'feature_type'
    score = 'score'
    suggested_class = 'suggested_class'
    other = 'other_CAPICE_value'


class OutputClasses(Enum):
    """
    Enums to use for the suggested output classes.
    """
    unknown = 'VUS'
    # Variables already defined for future implementation
    tolerated = ''
    likely_tolerated = ''
    likely_damaging = ''
    damaging = ''


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


class Versioning(Enum):
    VALIDATION_REGEX = (r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
                        r'(-?(?P<prerelease>a|b|rc[0-9]+))?$')
