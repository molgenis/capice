import logging
logger = logging.getLogger(__name__)
import pandas as pd
import os
from src.main.python.resources.utilities.utilities import get_project_root_dir,\
    load_modules, importer


class ManualAnnotator:
    def __init__(self):
        self.vep_annotators = []
        self.location = os.path.join(get_project_root_dir(),
                                     'src',
                                     'main',
                                     'python',
                                     'resources',
                                     'annotaters',
                                     'vep')
        self._load_vep_annotators()

    def _load_vep_annotators(self):
        python_modules = load_modules(self.location)
        self._check_n_modules(python_modules)
        loaded_python_modules = importer(python_modules, path=self.location)
        self._check_n_modules(loaded_python_modules)
        for module in loaded_python_modules:
            if 'name' in dir(module) and module.usable:
                self.vep_annotators.append(module)
        self._check_n_modules(self.vep_annotators)

    def _check_n_modules(self, modules_list):
        if len(modules_list) < 1:
            error_message = f'Unable to locate VEP Processors at {self.location}, ' \
                            'was the directory moved?'
            logger.critical(error_message)
            raise FileNotFoundError(error_message)

    def process(self, dataset: pd.DataFrame):
        for processor in self.vep_annotators:
            if processor.name in dataset.columns and processor.usable:
                self.log.debug('Processing: {}'.format(processor.name))
                dataset = processor.process(dataset)
                if processor.drop:
                    dataset.drop(columns=processor.name, inplace=True)
            else:
                logger.warning(
                    f'Could not use processor {processor.name} on input dataset!'
                )
        return dataset
