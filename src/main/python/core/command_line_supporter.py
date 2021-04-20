import argparse


class ArgumentParser:
    """
    Class to handle the given command line input.
    Type python3 capice.py --help for more details.
    """

    def __init__(self, description):
        self.description = description
        parser = self._create_argument_parser()

        self.arguments = parser.parse_args()

    def _create_argument_parser(self):
        """
        Parser function for 'capice.py' and all it's command line arguments.
        :return: parser
        """
        parser = argparse.ArgumentParser(
            prog="capice.py",
            description=self.description)
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

        optional.add_argument('-v',
                              '--verbose',
                              action='store_true',
                              help='When called, will print verbose messages.')

        optional.add_argument('-f',
                              '--force',
                              action='store_true',
                              help='Overwrites output if it already exists. (NOT AVAILABLE FOR LOGGING)')

        optional.add_argument('--train',
                              action='store_true',
                              help='Future addition.')
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
