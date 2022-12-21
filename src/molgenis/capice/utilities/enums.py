from enum import Enum


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
