from pathlib import Path
from abc import ABCMeta, abstractmethod
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.Validators import InputValidator
from src.main.python.resources.processors.input_processor import InputProcessor


class ArgsHandlerParent(metaclass=ABCMeta):
    def __init__(self, parser):
        self._call_loc = str(Path('.').absolute())
        self.parser = parser

    @property
    @abstractmethod
    def _extension(self):
        return ()

    @abstractmethod
    def create(self):
        pass

    def handle(self):
        self.parser.set_defaults(func=self._handle_args)

    def _handle_args(self, args):
        validator = InputValidator(self.parser)
        input_loc = args.input[0]
        validator.validate_input_loc(
            input_loc,
            extension=self._extension
        )
        output_path = None
        if args.output is not None:
            output_path = args.output[0]
        processor = InputProcessor(
            call_dir=self._call_loc,
            input_path=input_loc,
            output_path=output_path,
            force=args.force
        )
        output_loc = processor.get_output_directory()
        validator.validate_output_loc(output_loc)
        output_filename = processor.get_output_filename()
        self._handle_module_specific_args(
            input_loc, output_loc, output_filename, args
        )

    @abstractmethod
    def _handle_module_specific_args(self,
                                     input_loc,
                                     output_loc,
                                     output_filename,
                                     args):
        pass
