import os

import pandas as pd

from src.main.python.core.logger import Logger
from src.main.python.utilities.dynamic_loader import DynamicLoader
from src.main.python.utilities.utilities import get_project_root_dir


class ManualVEPProcessor:
    """
    Class ManualVEPProcessor, to process the (unusable) VEP-like features to
    features that are more usable.
    """

    def __init__(self):
        self.log = Logger().logger

    def process(self, dataset: pd.DataFrame):
        """
        Callable method for the ManualVEPProcessor to start processing.
        Loads all the VEP processors dynamically from /src/main/python/vep.
        :param dataset: pandas.DataFrame: loaded pandas dataframe of the user
        provided input TSV.
        :return: pandas.DataFrame: dataframe with processed features
        """
        self.log.info('Starting manual VEP feature processing.')
        vep_annotators = self._load_vep_processors()
        n_feats_processed = 0
        for processor in vep_annotators:
            if processor.name in dataset.columns and processor.usable:
                self.log.debug('Processing: %s', processor.name)
                dataset = processor.process(dataset)
                if processor.drop:
                    dataset.drop(columns=processor.name, inplace=True)
                n_feats_processed += 1
            else:
                self.log.warning('Could not use processor %s on input dataset!', processor.name)
        self.log.info('Processing successful.')
        self.log.debug('Processed %d features.', n_feats_processed)
        return dataset

    def _load_vep_processors(self):
        location = os.path.join(get_project_root_dir(), 'src', 'main', 'python', 'vep')
        self.log.debug('Loading modules at %s', location)
        loader = DynamicLoader(required_attributes=['name', 'process'], path=location)
        loaded_modules = loader.load_manual_annotators()
        self.log.debug('Loaded %d modules.', len(loaded_modules))
        return loaded_modules
