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
        self.feature_processing_tracker = {}

    def process(self, dataset: pd.DataFrame, process_features: list[str]) -> pd.DataFrame:
        """
        Callable method for the ManualVEPProcessor to start processing.
        Loads all the VEP processors dynamically from /src/main/python/vep.

        Args:
            dataset: The input dataset over which the VEP features should be processed.
            process_features: A collection of all input features that should be used in either
                              training or predicting over which VEP processing should happen.

        Returns:
            pandas.DataFrame: The input dataset, processed on the consequences

        """
        self.log.info('Starting manual VEP feature processing.')
        vep_annotators = self._load_vep_processors()
        dropping_columns = []
        n_feats_processed = 0
        for processor in vep_annotators:
            if (
                    processor.name in dataset.columns and
                    processor.name in process_features and
                    processor.usable
            ):
                self.log.debug('Processing: %s', processor.name)
                self._add_feature_tracking(processor.name, processor.columns)
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

    def _add_feature_tracking(self, processor_name: str, processor_features: list[str]):
        if processor_name not in self.feature_processing_tracker.keys():
            self.feature_processing_tracker[processor_name] = processor_features
        else:
            self.feature_processing_tracker[processor_name].extend(processor_features)

    def get_feature_processes(self) -> dict[str, list[str]]:
        """
        Getter for the dictionary containing all the processed features and their output features.

        Returns:
            dict:
                Input VEP processing features (key) and their output features (values)
        """
        return self.feature_processing_tracker

    def _load_vep_processors(self):
        location = os.path.join(get_project_root_dir(), 'vep')
        self.log.debug('Loading modules at %s', location)
        loader = DynamicLoader(required_attributes=['name', 'process'], path=location)
        loaded_modules = loader.load_manual_annotators()
        self.log.debug('Loaded %d modules.', len(loaded_modules))
        return loaded_modules
