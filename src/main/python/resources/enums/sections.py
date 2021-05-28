from enum import Enum


class Sections(Enum):
    DEFAULTS = 'DEFAULTS'
    OVERWRITES = 'OVERWRITES'
    MISC = 'MISC'
    TRAINING = 'TRAINING'


class Column(Enum):
    chr_pos_ref_alt = 'chr_pos_ref_alt'
    GeneName = 'GeneName'
    FeatureID = 'FeatureID'
    Consequence = 'Consequence'
    probabilities = 'probabilities'
