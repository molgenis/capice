"""
This is a helper script to balance out an input dataset.
Requires columns (%)Consequence and *_AF.
(%)Consequence: The consequence a variant has (Del, ins, DELINS etc.).
    Can be supplied raw (starting with %) or processed. The most important part
    is Consequence itself.
MAX_AF: The desired allele frequency per variant. Can originate from gnomAD or
1000 genomes or NHLBI-ESP, but has to be named MAX_AF.

"""
import os
import argparse
import numpy as np
import pandas as pd


def main():
    # To be filled in
    pass


class ArgumentParser:
    """
    Class to parse the input arguments.
    """
    def __init__(self):
        parser = self._create_argument_parser()
        self.arguments = parser.parse_args()

    @staticmethod
    def _create_argument_parser():
        parser = argparse.ArgumentParser(
            prog=os.path.basename(__file__),
            description='Helper script to balance out an possible input '
                        'dataset on allele frequency and Consequence. Requires '
                        'the columns (%)Consequence, (%)MAX_AF and '
                        'binarized_label. MAX_AF can originate from anywhere, '
                        'as long as it is called MAX_AF. Note: when -s/--split '
                        'is called, it will split before balancing.'
        )

        parser.add_argument(
            '-i',
            '--input',
            nargs=1,
            type=str,
            required=True,
            help='The input file location. Must be TSV or gzipped TSV!'
        )
        parser.add_argument(
            '-o',
            '--output',
            nargs=1,
            type=str,
            required=True,
            help='The output directory in which the files should be placed.'
        )
        parser.add_argument(
            '-s',
            '--split',
            action='store_true',
            help='Whenever the input dataset should be split into 20% '
                 'validation and 80% train/test.'
        )

        return parser

    def get_argument(self, argument_key):
        """
        Method to get an input argument.
        :param argument_key: Full command line argument (so --input for the
        input argument).
        :return: List or boolean
        """
        if self.arguments is not None and argument_key in self.arguments:
            value = getattr(self.arguments, argument_key)
        else:
            value = None
        return value


class Validator:
    """
    Class to check if arguments are valid.
    """



if __name__ == '__main__':
    main()
