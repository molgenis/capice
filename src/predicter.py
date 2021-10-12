from src.main_capice import Main
from src.__version__ import __version__
from src.main.python.core.config_reader import ConfigReader


class Predicter:
    def __init__(self, input_path, model_path, output_path):
        self.input_path = input_path
        self.model_path = model_path
        self.output_path = output_path

    def predict(self):
        config_reader = ConfigReader()
        config_reader.parse()
        Main(
            __program__='PoC',
            __version__=__version__,
            __author__='DH, RS, SvdH',
            input_loc=self.input_path,
            output_loc=self.output_path
        ).run()
