from src.main.python.core.logger import Logger
import pandas as pd
import os
from src.main.python.resources.utilities.dynamic_loader import DynamicLoader
from src.main.python.resources.utilities.utilities import get_project_root_dir


class ManualAnnotator:
    def __init__(self):
        self.log = Logger().logger

    def process(self, dataset: pd.DataFrame):
        vep_annotators = self._load_vep_processors()
        for processor in vep_annotators:
            if processor.name in dataset.columns and processor.usable:
                self.log.debug('Processing: %s', processor.name)
                dataset = processor.process(dataset)
                if processor.drop:
                    dataset.drop(columns=processor.name, inplace=True)
            else:
                self.log.warning(
                    'Could not use processor %s on input dataset!',
                    processor.name
                )
        return dataset

    @staticmethod
    def _load_vep_processors():
        location = os.path.join(
            get_project_root_dir(),
            'src',
            'main',
            'python',
            'resources',
            'annotaters',
            'vep'
        )
        loader = DynamicLoader(
            required_attributes=['name', 'process'],
            path=location
        )
        return loader.load_manual_annotators(
        )
