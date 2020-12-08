import argparse


class ArgumentSupporter:
    """
    Class to handle the given command line input.
    Type python3 capice.py --help for more details.
    """

    def __init__(self):
        parser = self._create_argument_parser()
        self.arguments = parser.parse_args()

    @staticmethod
    def _create_argument_parser():
        parser = argparse.ArgumentParser(
            prog="capice.py",
            description="The CAPICE pathogenic predictive model,"
                        " by Shuang et al.")
        required = parser.add_argument_group("Required arguments")
        optional = parser.add_argument_group("Optional arguments")

        required.add_argument('-i',
                              '--input',
                              nargs=1,
                              type=str,
                              required=True,
                              help='The location of the CADD'
                                   ' annotated SNV file.')

        required.add_argument('-o',
                              '--output',
                              nargs=1,
                              type=str,
                              required=True,
                              help='The output directory to put the processed'
                                   'CADD variants in. If no filename is given,'
                                   'will output to '
                                   'CAPICE_Predictions_HHMMSSMS_DDMMYYYY.'
                                   'tsv.gz')

        optional.add_argument('-l',
                              '--log_file',
                              nargs=1,
                              type=str,
                              default=None,
                              required=False,
                              help='The location to put the logfile in. '
                                   '(by default uses the directory of '
                                   '--output)')

        optional.add_argument('-gb',
                              '--genome_build',
                              nargs=1,
                              type=int,
                              default=False,
                              required=False,
                              help='The used Genome Build to generate the '
                                   'CADD file with.')

        optional.add_argument('-cb',
                              '--cadd_build',
                              nargs=1,
                              type=str,
                              default=False,
                              required=False,
                              help='The CADD version that was used to annotate.'
                                   ' (if not stated in the CADD file.)')

        optional.add_argument('-v',
                              '--verbose',
                              action='store_true',
                              help='When called, will print verbose messages.')

        optional.add_argument('-f',
                              '--force',
                              action='store_true',
                              help='Overwrites output if it already exists.')
        return parser

    def get_argument(self, argument_key):
        """
        Method to get a command line argument.
        :param argument_key: Command line argument.
        :return: List or string.
        """
        if self.arguments is not None and argument_key in self.arguments:
            value = getattr(self.arguments, argument_key)
        else:
            value = None

        return value
