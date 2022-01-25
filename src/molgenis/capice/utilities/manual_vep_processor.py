import os

import pandas as pd

from molgenis.capice.core.logger import Logger
from molgenis.capice.utilities import get_project_root_dir
from molgenis.capice.utilities.dynamic_loader import DynamicLoader


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
        dropping_columns = []
        n_feats_processed = 0
        for processor in vep_annotators:
            if processor.name in dataset.columns and processor.usable:
                self.log.debug('Processing: %s', processor.name)
                dataset = processor.process(dataset)
                if processor.drop and processor.name not in dropping_columns:
                    dropping_columns.append(processor.name)
                n_feats_processed += 1
            else:
                self.log.warning('Could not use processor %s on input dataset!', processor.name)
        self.log.debug('Property drop was set True for columns: %s', ', '.join(dropping_columns))
        dataset.drop(columns=dropping_columns, inplace=True)
        self.log.info('Processing successful.')
        self.log.debug('Processed %d features.', n_feats_processed)
        return dataset

    def _load_vep_processors(self):
        location = os.path.join(get_project_root_dir(), 'vep')
        self.log.debug('Loading modules at %s', location)
        loader = DynamicLoader(required_attributes=['name', 'process'], path=location)
        loaded_modules = loader.load_manual_annotators()
        self.log.debug('Loaded %d modules.', len(loaded_modules))
        return loaded_modules
