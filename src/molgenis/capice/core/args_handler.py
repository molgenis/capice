import logging
import argparse

from molgenis.capice import __version__
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.cli.args_handler_train import ArgsHandlerTrain
from molgenis.capice.cli.args_handler_predict import ArgsHandlerPredict
from molgenis.capice.cli.args_handler_explain import ArgsHandlerExplain


class ArgsHandler:
    """
    Command-line argument handler.
    Creates, initializes and calls the specific (predict, train etc.) module
    sub-parser.
    """

    def __init__(self):
        self.version = __version__
        self.parser = argparse.ArgumentParser(
            description="CAPICE, a machine-learning-based method for prioritizing pathogenic"
                        " variants https://doi.org/10.1186/s13073-020-00775-w"
        )
        self.manager = CapiceManager()

    def handle(self):
        """
        Method to handle the non module specific command line arguments. After
        argument handling, calls the module
        """
        args = self.parser.parse_args()
        self._handle_args(args)
        if 'func' in args:
            args.func(args)
        else:
            self.parser.print_help()
            self.parser.exit(2)

    def create(self):
        """
        Classmethod to create the ArgsHandler ArgumentParser instance
        and adds the subparsers to ArgsHandler. Does not automatically handle
        the input arguments, please use ArgsHandler.create().handle() for that.
        """
        self._add_arguments()
        subparsers = self.parser.add_subparsers()
        predictor = ArgsHandlerPredict(subparsers.add_parser('predict'))
        predictor.create()
        predictor.handle()
        trainer = ArgsHandlerTrain(subparsers.add_parser('train'))
        trainer.create()
        trainer.handle()
        explainer = ArgsHandlerExplain(subparsers.add_parser('explain'))
        explainer.create()
        explainer.handle()

    def _add_arguments(self):
        self.parser.add_argument(
            '-v',
            '--verbose',
            action='count',
            default=0,
            help='verbose mode. multiple -v options increase the verbosity')

        self.parser.add_argument(
            '--version',
            action='version',
            version=f'%(prog)s {self.version}'
        )

    def _handle_args(self, args):
        level = None
        if args.verbose == 1:
            level = logging.INFO
        elif args.verbose >= 2:
            level = logging.DEBUG
        self.manager.loglevel = level
