from src.main_capice import Main
from src.__version__ import __version__
from src.main.python.core.config_reader import ConfigReader
from src.main.python.core.global_manager import CapiceManager


class Predicter:
    def __init__(self, input_path, model_path, output_path):
        self.input_path = input_path
        self.model_path = model_path
        self.output_path = output_path

    def predict(self):
        config_reader = ConfigReader()
        config_reader.parse()
        manager = CapiceManager()
        manager.overwrite_impute = config_reader.get_overwrite_value(
            key='imputefile'
        )
        manager.overwrite_model = config_reader.get_overwrite_value(
            key='modelfile'
        )
        manager.config_vep_version = config_reader.get_default_value(
            key='vepversion'
        )
        manager.config_grch_build = config_reader.get_default_value(
            key='genomebuild'
        )

        Main(
            __program__='PoC',
            __version__=__version__,
            __author__='DH, RS, SvdH',
            input_loc=self.input_path,
            output_loc=self.output_path
        ).run()
