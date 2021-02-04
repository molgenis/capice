import argparse


class ArgumentSupporter:
    """
    Class to handle the given command line input.
    Type python3 capice.py --help for more details.
    """

    def __init__(self, description, type_cmd):
        self.description = description
        if type_cmd == 'main':
            parser = self._create_argument_parser_main()
        else:
            parser = self._create_argument_parser_train()
        self.arguments = parser.parse_args()

    def _create_argument_parser_main(self):
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
                              help='Overwrites output if it already exists. (NOT AVAILABLE FOR LOGGING)')

        optional.add_argument('--overwrite_impute_file',
                              nargs='+',
                              type=str,
                              default=None,
                              required=False,
                              help='The exact name (with spaces and capital letters) of the output of the get_name() '
                                   'function of an imputing datafile to be used in the CAPICE run.')

        optional.add_argument('--overwrite_model_file',
                              nargs='+',
                              type=str,
                              default=None,
                              required=False,
                              help='The exact name (with spaces and capital letters) of the output of the '
                                   'get_name() output of the model file to be used in the CAPICE run.')

        optional.add_argument('--disable_logfile',
                              action='store_true',
                              help='Disable the creation of the logfile. Will still output all logging to stdout and'
                                   'stderr.')
        return parser

    def _create_argument_parser_train(self):
        parser = argparse.ArgumentParser(
            prog="train_capice_model.py",
            description=self.description)

        required = parser.add_argument_group("Required arguments")
        optional = parser.add_argument_group("Optional arguments")

        required.add_argument('-i',
                              '--input',
                              nargs=1,
                              type=str,
                              default=None,
                              required=False,
                              help='The location of the TSV training file. '
                                   'Will be made balanced, '
                                   'this balanced dataset will '
                                   'be output to -o. '
                                   'Will cause bias if training '
                                   'file contains indexing numbers. If you do not want the dataset to be balanced, use'
                                   ' the -bi / balanced_input flag.')

        optional.add_argument('-bi',
                              '--balanced_input',
                              nargs=1,
                              type=str,
                              default=None,
                              help='Use this argument if you already have a '
                                   'balanced dataset or dont\'t want to use '
                                   'a balanced dataset.')

        required.add_argument('-o',
                              '--output',
                              nargs=1,
                              type=str,
                              required=True,
                              help='The output directory to put the models in.')

        optional.add_argument('-l',
                              '--log_file',
                              nargs=1,
                              type=str,
                              default=None,
                              required=False,
                              help='The location to put the logfile in. '
                                   '(by default uses the directory of '
                                   '--output)')

        optional.add_argument('-d',
                              '--default',
                              action='store_true',
                              help='Use the python3.6 model hyperparameters.')

        optional.add_argument('-v',
                              '--verbose',
                              action='store_true',
                              help='Prints messages if called.')

        optional.add_argument('-sd',
                              '--specified_default',
                              type=str,
                              nargs=1,
                              help='The location of a json containing "default" hyperparameters: learning_rate, '
                                   'n_estimators and max_depth.')

        optional.add_argument('-s',
                              '--split',
                              default=False,
                              type=float,
                              help='Split the data into a training and test set before any processing happens.'
                                   ' Requires a float percentage (0-1).')

        optional.add_argument('-ttsize',
                              '--train_test_size',
                              default=0.2,
                              type=float,
                              help='Argument to be passed to the train test split that will be used to determine '
                                   'the size of the test dataset (in percentage) used within the training process. '
                                   'Requires a float percentage (0-1).')

        optional.add_argument('-e',
                              '--exit',
                              action='store_true',
                              help="Activate early exit, right after creating the balanced dataset (if -i is used),"
                                   " but before any preprocessing or training happens")

        required.add_argument('--overwrite_impute_file',
                              nargs='+',
                              type=str,
                              default=None,
                              required=True,
                              help='The exact name (with spaces and capital letters) of the output of the get_name() '
                                   'function of an imputing datafile to be used in the CAPICE run.')

        optional.add_argument('-f',
                              '--force',
                              action='store_true',
                              help='Overwrites output if it already exists. (NOT AVAILABLE FOR LOGGING)')

        optional.add_argument('--disable_logfile',
                              action='store_true',
                              help='Disable the creation of the logfile. Will still output all logging to stdout and'
                                   'stderr.')
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
