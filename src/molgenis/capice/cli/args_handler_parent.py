import os
from abc import ABCMeta, abstractmethod

import xgboost as xgb

from molgenis.capice import __version__
from molgenis.capice.utilities.input_processor import InputProcessor
from molgenis.capice.validators.input_validator import InputValidator
from molgenis.capice.validators.version_validator import VersionValidator


class ArgsHandlerParent(metaclass=ABCMeta):
    """
    Parent class of all module specific argument parsers / handlers.
    """

    def __init__(self, parser):
        self.parser = parser
        self.input_validator = InputValidator()

    @property
    @abstractmethod
    def _extension(self) -> tuple[str]:
        """
        Property to define what extension(s) are allowed for an input file for
        each module parser.
        """
        pass

    def _extension_str(self) -> str:
        """
        String representation of `_extension()`
        """
        return self._join_extensions(self._extension)

    @property
    @abstractmethod
    def _required_output_extensions(self) -> tuple[str]:
        """
        Property to define what the output file extensions are allowed for each
        module parser.
        """
        pass

    def _required_output_extensions_str(self) -> str:
        """
        String representation of `_required_output_extensions()`
        """
        return self._join_extensions(self._required_output_extensions)

    @property
    @abstractmethod
    def _empty_output_extension(self) -> str:
        """
        Property to define what extension an output file should get if no
        output file extension was given.

        Preferably, use: self._required_output_extensions[<value>]
        """
        pass

    @abstractmethod
    def create(self):
        """
        Method to define what parser options should be available for the module.
        Use self.parser.add_argument() to add an argument to the subparser.
        """
        pass

    def handle(self):
        """
        Superclass handler to set the arguments set in create(). Also calls the
        parser to proceed with parsing the module specific arguments, validate
        them and run  the CAPICE code.
        """
        self.parser.set_defaults(func=self._handle_args)

    def _handle_args(self, args):
        """
        Superclass handle args to parse and validate the input and output
        arguments. Also parses the output filename.
        """
        version_validator = VersionValidator()
        try:
            version_validator.validate_capice_version(__version__)
        except ValueError as cm:
            self.parser.error(str(cm))
        input_path = self._retrieve_argument_from_list(args.input, '-i/--input')
        try:
            self.input_validator.validate_input_path(input_path, extension=self._extension)
        except FileNotFoundError as cm:
            self.parser.error(str(cm))
        output_path = self._retrieve_argument_from_list(args.output, '-o/--output')
        try:
            processor = InputProcessor(
                input_path=input_path,
                output_path=output_path,
                force=args.force,
                default_extension=self._empty_output_extension
            )
        except FileExistsError as cm:
            self.parser.error(str(cm))
        output_filename = processor.get_output_filename()
        output_filename = self._handle_output_filename(output_filename)
        output_given = processor.get_output_given()
        output_path = processor.get_output_directory()
        try:
            self.input_validator.validate_output_path(output_path)
        except OSError as cm:
            self.parser.error(str(cm))
        self._handle_module_specific_args(input_path, output_path, output_filename, output_given,
                                          args)

    def _retrieve_argument_from_list(self,
                                     arg: list | None,
                                     arg_name: str,
                                     has_default: bool = False) -> None | str:
        try:
            return self._single_argument_retriever(arg, arg_name, has_default)
        except IOError as e:
            self.parser.error(e)
            return None

    @staticmethod
    def _single_argument_retriever(arg: list | None,
                                   arg_name: str,
                                   has_default: bool) -> None | str:
        """
        Retrieves the user-argument from a list. It requires the user to have only entered
        the argument once (combined with `action='append'` for argument parsing), resulting in a
        list of length:
         - 0 (no arguments given & no default value)
         - 1 (1 argument given or default_value is present)
         - 2 (1 argument given and default value present)

         If `has_default`==True, the first list item is assumed to be the default one (set through
         `default=[<value>]`) and any extra items in the list being user-input.

        Args:
            arg: List of arguments (or None if no arguments where generated and no defaults were
            present either)
            arg_name: The name of the user-argument to which `arg` belongs
            has_default: whether a default arg is present in the given arg list
        Returns:
            None (if args is None) or a single item from the given list.
        Raises:
            ValueError: If empty list is given (=programming error)
            IOError: If list contains more items than expected (>2 if has_default, else >1).

        """
        # None is simply returned.
        if arg is None:
            return arg

        arg_len = len(arg)

        # Empty list indicates programming bug.
        if arg_len == 0:
            raise ValueError('Empty list is given. Should be None or list with elements.')

        # Retrieve value to be used for CLI argument.
        if arg_len > 2 or (arg_len > 1 and not has_default):
            raise IOError(f'Argument {arg_name} is only allowed once.')
        else:
            return arg[arg_len-1]

    @abstractmethod
    def _handle_module_specific_args(self, input_path, output_path, output_filename, output_given,
                                     args):
        """
        Method to be filled in by the module specific parsers. Should perform
        additional validation over args specific to the parser. Should then call
        the module to continue the module.
        """
        pass

    def _handle_output_filename(self, output_filename: str):
        """
        Method to validate that an output filename complies with the
        required output extension.
        """
        if '.' in output_filename and not output_filename.endswith(
                self._required_output_extensions):
            self.parser.error(
                f'Output file extension is incorrect. Expected output extension: '
                f'{self._required_output_extensions}'
            )
        else:
            return output_filename

    @staticmethod
    def load_model(model_path: os.PathLike) -> xgb.XGBClassifier:
        model = xgb.XGBClassifier()
        model.load_model(model_path)
        return model

    @staticmethod
    def _join_extensions(extensions: tuple[str]) -> str:
        return ', '.join(extensions)
