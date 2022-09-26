"""
This is a helper script to balance out an input dataset.
Requires columns (%)Consequence and *_AF.
(%)Consequence: The consequence a variant has (Del, ins, DELINS etc.).
    Can be supplied raw (starting with %) or processed. The most important part
    is Consequence itself.
gnomAD_AF: The desired allele frequency per variant. Can originate from gnomAD or
1000 genomes or NHLBI-ESP, but has to be named gnomAD_AF.

"""
import os
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

__random_state__ = 5
__bins__ = [0.0, 0.01, 0.05, 0.1, 0.5, 1.0]


def correct_column_names(dataset):
    new_columns = []
    for col in dataset.columns:
        if col.startswith('%'):
            new_columns.append(col.split('%')[1])
        elif col.startswith('#'):
            new_columns.append(col.split('#')[1])
        else:
            new_columns.append(col)
    dataset.columns = new_columns
    return dataset


def main():
    # Parse CLA
    cla_parser = ArgumentParser()
    input_path = cla_parser.get_argument('input')[0]
    output_directory = cla_parser.get_argument('output')[0]
    split = cla_parser.get_argument('split')
    # Validate CLA
    cla_validator = CommandLineArgumentsValidator()
    cla_validator.validate_input_path(input_path)
    cla_validator.validate_output_directory(output_directory)
    # Load in dataset
    dataset = pd.read_csv(input_path, na_values='.', sep='\t', low_memory=False)
    dataset = correct_column_names(dataset)
    # Validate dataset
    dataset_validator = InputDatasetValidator()
    dataset_validator.validate_columns_required(dataset)
    dataset_validator.validate_b_p_present(dataset)
    # Run
    exporter = BalanceExporter(output_path=output_directory)
    splitter = Split()
    if split:
        validation_dataset, dataset = splitter.split(dataset)
        # Export here so the splitter function is easier to test
        exporter.export_validation_dataset(validation_dataset)
    balancer = Balancer()
    balanced_dataset = balancer.balance(dataset)
    # Export
    exporter.export_train_test_dataset(balanced_dataset)


class ArgumentParser:
    """
    Class to parse the input arguments.
    """

    def __init__(self):
        parser = self._create_argument_parser()
        self.arguments = parser.parse_args()

    @staticmethod
    def _create_argument_parser():
        parser = argparse.ArgumentParser(
            prog=os.path.basename(__file__),
            description='Helper script to balance out an possible input '
                        'dataset on allele frequency and Consequence. Requires '
                        'the columns (%)Consequence, (%)gnomAD_AF and '
                        'binarized_label. gnomAD_AF can originate from anywhere, '
                        'as long as it is called gnomAD_AF. Note: when -s/--split '
                        'is called, it will split before balancing.'
        )

        parser.add_argument(
            '-i',
            '--input',
            nargs=1,
            type=str,
            required=True,
            help='The input file location. Must be TSV or gzipped TSV!'
        )
        parser.add_argument(
            '-o',
            '--output',
            nargs=1,
            type=str,
            required=True,
            help='The output directory in which the files should be placed.'
        )
        parser.add_argument(
            '-s',
            '--split',
            action='store_true',
            help='Whenever the input dataset should be split into 20% '
                 'validation and 80% train/test.'
        )

        return parser

    def get_argument(self, argument_key):
        """
        Method to get an input argument.
        :param argument_key: Full command line argument (so --input for the
        input argument).
        :return: List or boolean
        """
        if self.arguments is not None and argument_key in self.arguments:
            value = getattr(self.arguments, argument_key)
        else:
            value = None
        return value


class CommandLineArgumentsValidator:
    """
    Class to check if arguments are valid.
    """

    def validate_input_path(self, input_path):
        self._validate_input_exists(input_path)
        self._validate_input_extension(input_path)

    @staticmethod
    def _validate_input_exists(input_path):
        if not os.path.isfile(input_path):
            raise FileNotFoundError('Input file does not exist!')

    @staticmethod
    def _validate_input_extension(input_path):
        if not input_path.endswith(('.tsv', '.tsv.gz')):
            raise FileNotFoundError('Input file is not TSV or gzipped TSV!')

    def validate_output_directory(self, output_directory):
        self._validate_output_directory_parent_exists(output_directory)
        self._validate_output_parent_writable(output_directory)
        self._ensure_output(output_directory)

    @staticmethod
    def _validate_output_directory_parent_exists(output_directory):
        if (
                not os.path.isdir(output_directory)
                and not os.path.isdir(Path(output_directory).parent)
        ):
            raise OSError('Given output directory parent does not exist!')

    @staticmethod
    def _validate_output_parent_writable(output_directory):
        if (
                not os.path.isdir(output_directory)
                and not os.access(Path(output_directory).parent, os.W_OK)
        ):
            raise OSError('New directory can not be created in a read/execute only directory!')

    @staticmethod
    def _ensure_output(output_directory):
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)


class InputDatasetValidator:
    """
    Class to check if the input dataset is usable
    """

    @staticmethod
    def validate_columns_required(dataset: pd.DataFrame):
        required_columns = ['Consequence', 'gnomAD_AF', 'binarized_label']
        for col in required_columns:
            if col not in dataset.columns:
                raise KeyError(f'Required column {col} not found in input dataset.')

    @staticmethod
    def validate_b_p_present(dataset: pd.DataFrame):
        """
        Method to validate that at least one pathogenic and one benign sample is present
        """
        if dataset[dataset['binarized_label'] == 0].shape[0] == 0:
            raise ValueError('Not enough benign samples to balance!')
        if dataset[dataset['binarized_label'] == 1].shape[0] == 0:
            raise ValueError('Not enough pathogenic samples to balance!')


class Split:
    """
    Class dedicated to splitting the data into a validation dataset and a train/test dataset.
    """

    @staticmethod
    def split(dataset: pd.DataFrame):
        """
        Splits 10% of the pathogenic and 10% of the benign samples into a validation dataset
        and immediately exports said validation dataset. Returns the train-test dataset.
        """
        validation_dataset = pd.DataFrame(columns=dataset.columns)
        return_dataset = pd.DataFrame(columns=dataset.columns)
        # Benign
        all_benign = dataset[dataset['binarized_label'] == 0]
        all_benign._is_copy = None
        v_benign_samples = all_benign.sample(frac=0.1, random_state=__random_state__)
        # A bit cryptic to remove the random samples from the benign dataset, but it works
        all_benign = pd.concat([all_benign, v_benign_samples], axis=0, ignore_index=True)
        all_benign.drop_duplicates(keep=False, inplace=True)
        return_dataset = pd.concat([return_dataset, all_benign], axis=0, ignore_index=True)
        validation_dataset = pd.concat([validation_dataset, v_benign_samples], axis=0,
                                       ignore_index=True)

        # Pathogenic
        all_pathogenic = dataset[dataset['binarized_label'] == 1]
        all_pathogenic._is_copy = None
        v_patho_samples = all_pathogenic.sample(frac=0.1, random_state=__random_state__)
        # Again a cryptic way to remove the randomly samples pathogenic samples
        all_pathogenic = pd.concat([all_pathogenic, v_patho_samples], axis=0, ignore_index=True)
        all_pathogenic.drop_duplicates(keep=False, inplace=True)
        return_dataset = pd.concat([return_dataset, all_pathogenic], axis=0, ignore_index=True)
        validation_dataset = pd.concat([validation_dataset, v_patho_samples], axis=0,
                                       ignore_index=True)
        return validation_dataset, return_dataset


class Balancer:
    """
    Class dedicated to performing the balancing algorithm
    """

    def __init__(self):
        self.bins = __bins__
        self.columns = []

    def balance(self, dataset: pd.DataFrame):
        self.columns = dataset.columns
        pathogenic = dataset[dataset['binarized_label'] == 1]
        benign = dataset[dataset['binarized_label'] == 0]
        return_dataset = pd.DataFrame(columns=self.columns)
        for consequence in dataset['Consequence'].unique():
            selected_pathogenic = pathogenic[pathogenic['Consequence'] == consequence]
            selected_benign = benign[benign['Consequence'] == consequence]
            processed_consequence = self._process_consequence(
                pathogenic_dataset=selected_pathogenic, benign_dataset=selected_benign
            )
            return_dataset = pd.concat(
                [
                    return_dataset,
                    processed_consequence
                ], axis=0, ignore_index=True
            )
        return return_dataset

    def _process_consequence(self, pathogenic_dataset, benign_dataset):
        n_patho = pathogenic_dataset.shape[0]
        n_benign = benign_dataset.shape[0]
        if n_patho > n_benign:
            pathogenic_dataset = pathogenic_dataset.sample(
                n_benign,
                random_state=__random_state__
            )
        pathogenic_histogram, bins = np.histogram(
            pathogenic_dataset['gnomAD_AF'],
            bins=self.bins
        )
        processed_bins = pd.DataFrame(columns=self.columns)
        for ind in range(len(bins) - 1):
            lower_bound = bins[ind]
            upper_bound = bins[ind + 1]
            sample_number = pathogenic_histogram[ind]
            processed_bins = pd.concat(
                [
                    processed_bins,
                    self._process_bins(
                        pathogenic_dataset, benign_dataset, upper_bound, lower_bound, sample_number
                    )
                ], axis=0, ignore_index=True
            )
        return processed_bins

    def _process_bins(
            self, pathogenic_dataset, benign_dataset, upper_bound, lower_bound, sample_num
    ):
        selected_pathogenic = self._get_variants_within_range(
            pathogenic_dataset, upper_bound=upper_bound, lower_bound=lower_bound
        )
        selected_benign = self._get_variants_within_range(
            benign_dataset, upper_bound=upper_bound, lower_bound=lower_bound
        )
        if sample_num < selected_benign.shape[0]:
            return_benign = selected_benign.sample(
                sample_num,
                random_state=__random_state__
            )
            return_pathogenic = selected_pathogenic
        else:
            return_benign = selected_benign
            return_pathogenic = selected_pathogenic.sample(
                selected_benign.shape[0],
                random_state=__random_state__
            )
        return pd.concat(
            [return_benign, return_pathogenic], axis=0,  ignore_index=True
        )

    @staticmethod
    def _get_variants_within_range(dataset, upper_bound, lower_bound):
        return dataset[(dataset['gnomAD_AF'] >= lower_bound) & (dataset['gnomAD_AF'] < upper_bound)]


class BalanceExporter:
    """
    Class dedicated to exporting of splitting datasets and exporting of the balancing dataset.
    """

    def __init__(self, output_path):
        self.output_path = output_path

    def export_validation_dataset(self, dataset):
        self._export_dataset(dataset, 'validation.tsv.gz')

    def export_train_test_dataset(self, dataset):
        self._export_dataset(dataset, 'train_test_split.tsv.gz')

    def _export_dataset(self, dataset: pd.DataFrame, dataset_name: str):
        full_export = os.path.join(self.output_path, dataset_name)
        dataset.to_csv(
            path_or_buf=full_export, sep='\t', na_rep='.', index=False, compression='gzip'
        )
        print(f'Successfully exported {dataset_name} to {full_export}')


if __name__ == '__main__':
    main()
