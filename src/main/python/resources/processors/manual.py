import os
import pandas as pd
from src.main.python.core.logger import Logger
from src.main.python.resources.utilities.dynamic_loader import DynamicLoader
from src.main.python.resources.utilities.utilities import get_project_root_dir


class ManualProcessor:
    """
    Class ManualProcessor, to process the (unusable) VEP-like features to
    features that are more usable.
    """
    def __init__(self):
        self.log = Logger().logger

    def process(self, dataset: pd.DataFrame):
        """
        Callable method for the ManualProcessor to start processing. Loads all
        the VEP processors dynamically from
        /src/main/python/resources/processors/vep.
        :param dataset: pandas.DataFrame: loaded pandas dataframe of the user
        provided input TSV.
        :return: pandas.DataFrame: dataframe with processed features
        """
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
            'processors',
            'vep'
        )
        loader = DynamicLoader(
            required_attributes=['name', 'process'],
            path=location
        )
        return loader.load_manual_annotators(
        )
