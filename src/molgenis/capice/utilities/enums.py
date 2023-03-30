from enum import Enum


class InputColumn(Enum):
    """
    Columns within panda data frames.
    `col_name` is the column name as should be used within CAPICE after processing input.
    `col_input_name` is the expected name as given by the input file.

    If `col_name` and `col_input_name` are equal, the name does not get altered.
    """
    # General
    chr = ('chr', 'CHROM')
    pos = ('pos', 'POS')
    ref = ('REF', 'REF')
    alt = ('ALT', 'ALT')
    gene_name = ('gene_name', 'SYMBOL')
    gene_id = ('gene_id', 'Gene')
    gene_name_source = ('id_source', 'SYMBOL_SOURCE')  # see GitHub issue 169
    feature = ('feature', 'Feature')
    feature_type = ('feature_type', 'Feature_type')
    intron = ('Intron', 'INTRON')  # Combination of 2x int64 divided by a "/"
    exon = ('Exon', 'EXON')  # Combination of 2x int64 divided by a "/"

    # Train-only
    binarized_label = ('binarized_label', 'binarized_label')
    sample_weight = ('sample_weight', 'sample_weight')

    def __init__(self, col_name, col_input_name):
        self.col_name = col_name
        self.col_input_name = col_input_name


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


class UniqueSeparator(Enum):
    """
    Enum specific to creating a specific separator for the preservation of the chr pos ref alt
    columns.
    """
    unique_separator = '_VeryUniqueCAPICESeparator_'


class Versioning(Enum):
    VALIDATION_REGEX = (r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
                        r'(-?(?P<prerelease>a|b|rc[0-9]+))?$')
