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
        self.feature_processing_outputs = {}

    def process(self, dataset: pd.DataFrame, process_json: dict | None = None) -> pd.DataFrame:
        """
        Callable method for the ManualVEPProcessor to start processing.
        Loads all the VEP processors dynamically from /src/main/python/vep.

        Args:
            dataset: The input dataset over which the VEP features should be processed.
            process_json: The input train_features json.

        Returns:
            pandas.DataFrame: The input dataset, processed on the consequences

        """
        self.log.info('Starting manual VEP feature processing.')
        vep_annotators = self._load_vep_processors()
        if process_json is None:
            processable_features = dataset.columns
        else:
            processable_features = process_json.keys()
        dropping_columns = []
        n_feats_processed = 0
        for processor in vep_annotators:
            if (
                    processor.name in dataset.columns and
                    processor.name in processable_features and
                    processor.usable
            ):
                self.log.debug('Processing: %s', processor.name)
                self.feature_processing_outputs[processor.name] = processor.columns
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

    def get_feature_process_outputs(self) -> dict:
        """
        Getter for the dictionary containing the VEP feature (key) and
        the features that are processed out of that VEP feature (value)

        Returns:
            dict: VEP feature (key) and the features that origin from it (value)
        """
        return self.feature_processing_outputs

    def _load_vep_processors(self):
        location = os.path.join(get_project_root_dir(), 'vep')
        self.log.debug('Loading modules at %s', location)
        loader = DynamicLoader(required_attributes=['name', 'process'], path=location)
        loaded_modules = loader.load_manual_annotators()
        self.log.debug('Loaded %d modules.', len(loaded_modules))
        return loaded_modules
