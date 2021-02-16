# CAPICE : a computational method for Consequence-Agnostic Pathogenicity Interpretation of Clinical Exome variations

CAPICE is a computational method for predicting the pathogenicity of SNVs and InDels. 
It is a gradient boosting tree model trained using a variety of genomic annotations used by 
CADD score and trained on the clinical significance. CAPICE performs consistently across diverse independent synthetic, 
and real clinical data sets. It ourperforms the current best method in pathogenicity estimation
for variants of different molecular consequences and allele frequency.

The software can be used as web service, as pre-computed scores or by installing the software locally, all described below.

## Use online web service

CAPICE can be used as online service at http://molgenis.org/capice 

## Download files of precomputed scores for all possible SNVs and InDels (based on GrCh37 and CADD version 1.4)
We precomputed the CAPICE score for all possible SNVs and InDels. It can be downloaded via [zenodo](https://doi.org/10.5281/zenodo.3516248).

The file contains the following columns:

*#CHROM* chromosome name, as [1:22, X]

*POS* genomic position (GrCh37 genome assembly)

*REF* reference allele

*ALT* alternative allele

*score* CAPICE score. The score ranges from 0 to 1, the higher the more likely the variant is pathogenic

## Install CAPICE software locally
The CAPICE software is also provided in this repository for running CAPICE in your own environment. 
The following sections will guide you through the steps needed for the variant annotation and the execution of
making predictions using the CAPICE model.

### Download and installation

1. Software and libraries
CAPICE scripts can be downloaded from the CAPICE github repository.
```
git clone https://github.com/molgenis/capice.git
cd capice
```

1.1 Installation of libraries

The following libraries are required to run CAPICE in Python 3.6 (__NOTE__: These are __NOT__ supplied within the requirements.txt):

```
numpy | Version 1.13.3
pandas | Version 0.21.0
scipy | Version 1.0.1
scikit-learn | Version 0.19.1
xgboost | Version 0.72.1
```

For Python 3.7 and greater, the following libraries are required (and can be installed in a Python virtual environment using `venv_installer.sh`):
```
numpy | Version 1.18.1
pandas | Version 1.0.2
scikit-learn | Version 0.23.1
xgboost | Version 1.1.1
```

### Usage for predictions

CAPICE predictions can be run by using the following command:

`python3 capice.py` _arguments_

CAPICE requires the following arguments:

- -i / --input: The path to the input [CADD annotated](https://cadd.gs.washington.edu/) dataset using the tab separator (can be both gzipped or not). An example of an input TSV file can be found in `CAPICE_example/test_cadd14_grch37_annotated.tsv.gz` for CADD 1.4 and genome build 37.
- -o / --output: The path to the directory where the output is placed (will be made if it does not exists).

The following arguments are partially optional:

- -cb / --cadd_build: If no original header of the CADD output file is present then this argument requires a float (like 1.4) to tell CAPICE what CADD version was used to annotate the file.
- -gb / --genome_build: If no original header of the CADD output file is present then this argument requires an integer (like 37) to tell CAPICE what the Genome Build version was used to annotate the file.

The following arguments can be used to specifically select a certain model file or imputing file:

- --overwrite_impute_file: The full string (without quotation marks) of the return of the `get_name()` function within a certain imputing file.
- --overwrite_model_file: The full string (without quotation marks) of the return of the `get_name()` function within a certain model file.

The following flags can be added:

- -v / --verbose: Display more in depth messages within the progress of CAPICE.
- -f / --force: Overwrite an output file if already present (does NOT work for logfiles).
- -l / --log_file: Path to a directory where log files are stored. Will be made if it does not exists. Default is in the output directory.
- --disable_logfile: Flag to disable the creation of a logfile. Will output to STDout and STDerr.

#### Output of CAPICE prediction files

A file will be put out containing the following columns:

- __No__ index
- chr_pos_ref_alt: column containing the chromosome, position, reference and alternative separated by an underscore.
- ID: Column full of `.`.
- GeneName: The ENSEMBL gene name of the variant as supplied by CADD.
- FeatureID: The ENSEMBL feature ID (Transcript ID or regulatory feature ID).
- Consequence: The type of consequence that the variant has as supplied by CADD.
- probabilities: The predicted CAPICE score for the variant. The higher the score, the more likely that the variant is pathogenic.

### Usage for making new CAPICE like models

Outside of Predictions, this repository also provides users the availability to create new CAPICE like models according to their specific use case.
Unlike CAPICE Predictions, this input file is fully dependent on the imputing file used to impute the input dataset, but requires 2 columns at the very least: `sample_weight` and `binarized_label`.
Sample weight can be 1 for all samples if no sample weight should be applied. Binarized label should be either 0 or 1, depending on your labels of classification. 
_Note: when applying balancing to the input dataset, only a 2 class problem can be processed._

To make new CAPICE like models, run the following command:

`python3 train_model.py` _arguments_

The following arguments are required:

- -i / --input: Path to a input dataset in TSV format.
- -o / --output: Path to an output directory. Will be made if it does not exists.
- --overwrite_impute_file: The full string (without quotation marks) of the return of the `get_name()` function within a certain imputing file.

The following arguments are optional:

- -b / --balance: Flag to be added when the input dataset is required to be balanced on Allele frequency, consequence and the distribution of pathogenic and benign samples.
- -l / --log_file: Path to a directory in where log files are stored. Will be made if it does not exists. Default will be within the output directory.
- -d / --default: Flag to be added when the originally published hyper parameters should be used to create a new model.
- -sd / --specified_default: Path to a JSON containing the 3 tunable hyper parameters: `learning_rate` (in float), `max_depth` (in integer) and `n_estimators` (in integer). If both -d and -sd are called, -sd will overrule -d.
- -s / --split: Float that defines a split of the input data before any processing happens, but after balancing happens (if called). Use this flag if you want to create a benchmarking / validating dataset out of the initial input dataset.
- -ttsize / --train_test_size: Float that defines what percentage of the processed data will be used as test dataset once the model is actually training.
- -e / --exit: Flag to be called if the program should exit right after balancing (if called), splitting (using -s, if called) and the loading of default hyper parameters (if called) for testing purposes or for data preparation purposes.
- -f / --force: Flag to be called if output files should be overwritten if they exist.
- --disable_logfile: Flag to be called if the creation of a logfile is not wanted.

###### Examples:

- Balance out the given file and make an XGBoost model on the balanced set using the originally published hyper parameters, while logging more messages:
    - `python3 train_model.py -i path/to/cadd/annotated/file -o path/to/output -b -d -v` 

- Do not balance out the given dataset and split it to a 90% dataset to be used for imputing, preprocessing and training. The remaining 10% could be used for later validation:
    - `python3 train_model.py -i path/to/balanced/cadd/annotated/file -o path/to/output -v -s 0.1`

- Make a model using previously found optimal hyper parameters, without balancing out the input dataset, while using 90% of the input dataset for training:
    - `python3 train_model.py -i path/to/cadd/annotated/file -o path/to/output -v -s 0.1 -sd path/to/hyperparameters.json`
    
- Balance out and split a dataset, without training:
    - `python3 train_model.py -i path/to/cadd/annotated/file -o path/to/output -s 0.1 -v -e`

#### Outputs for training a new model:

For datasets exported during the training procedure:

- Your dataset will still remain the same as the input in terms of columns. When the balancing argument is called, the output balance dataset will be balanced on `Consquence`, `max_AF` and on `binarized_label`.
If split is used, the output data will be `(1-argument) * 100%` the size of your input data.

For models exported during the training procedure:

- If the filename starts with `xgb_classifier`: [Pickled](https://docs.python.org/3/library/pickle.html) instance of a [XGBClassifier](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier) instance that has successfully trained on the input data.
- If the filename starts with `randomized_search_cv`: [Pickled](https://docs.python.org/3/library/pickle.html) instance of a [RandomizedSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html) instance that has successfully identified optimal hyper parameters for a new CAPICE like model.

_Note: to load in a pickled instance of a model, use the following commands:_
```
import pickle
model = pickle.load(open(path/to/model_file.pickle.dat, 'rb'))
```

## FAQ:

- Will CAPICE support CADD 1.6 and Genome Build 38?

In a future patch CAPICE will add support for CADD 1.6 and Genome Build 38, for both CADD 1.4 and CADD 1.6.

- These scores are nice and all, but what do they really mean for this particular variant?

CAPICE bases it's scoring on the training that it was provided with. A score is assigned based on features the model learned to recognize during training.
There are plans to make a "Capice Explain Tool" which will tell how a score came to be.

- Training a new model failed with an error in `joblib.externals.loky.process_executor.RemoteTraceback` with `ValueError: unknown format is not supported`. Why?

This could possibly originate from a low sample size during the cross validation in RandomSearchCV. Please [contact](https://github.com/molgenis/capice/issues) us for further help.
  



