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

### Download and installation (UNIX like systems)
__Note: this install is for Python 3.7, Python 3.8 and Python 3.9. 
The install instructions for Python 3.6 can be found at the bottom of this chapter.
Python 3.5 and lower is not supported.__

1. Software and libraries
CAPICE scripts can be downloaded from the CAPICE github repository.
```
git clone https://github.com/molgenis/capice.git
cd capice
```

#### 1.1 Installation of libraries

CAPICE can be installed through the supplied setup.py.

```
pip install .
```

If you do not have admin rights, a virtual environment can be used as well, which can be installed as following:

```
bash venv_installer.sh
```

Alternatively, individual packages can be installed manually through `pip install`:

```
numpy | Version 1.20.2
pandas | Version 1.2.4
scipy | Version 1.6.2
scikit-learn | Version 0.24.2
xgboost | Version 0.90
```

`pip install numpy==1.20.2 pandas==1.2.4 scipy==1.6.2 scikit-learn==0.24.2 xgboost==0.90`

For Python 3.6, the following packages have to be manually installed:

```
numpy | Version 1.13.3
pandas | Version 0.21.0
scipy | Version 1.0.1
scikit-learn | Version 0.19.1
xgboost | Version 0.72.1 (Version 0.90 also works)
```

`pip install numpy==1.13.3 pandas==0.21.0 scipy==1.0.1 scikit-learn==0.19.1 xgboost==0.72.1`

__Installation on Windows systems is not possible. Please refer to UNIX like systems (iOS or Linux) or use the [Windows subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).__

#### 1.2 Additional required files

CAPICE requires a [Faidx indexed fasta file](http://www.htslib.org/doc/samtools-faidx.html), with contigs 1-22, X, Y and MT. We recommend the [1000genomes reference fasta](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/) (both `human_g1k_v37.fasta.gz` and `human_g1k_v37.fasta.gz.fai` are required) (MD5sum can be found [here](https://gatk.broadinstitute.org/hc/en-us/articles/360035890711-GRCh37-hg19-b37-humanG1Kv37-Human-Reference-Discrepancies)).
Once the reference fasta and it's Faidx index have been created, set the location of the fasta file in `config.cfg`.

### Usage

CAPICE predictions can be run by using the following command:

`python3 capice.py` _arguments_

CAPICE requires the following arguments:

- -i / --input: The path to the input [VEP annotated](https://www.ensembl.org/info/docs/tools/vep/index.html) dataset using the tab separator (can be both gzipped or not). An example of an input TSV file can be found in `CAPICE_example/CAPICE_input.tsv.gz` for genome build 37. The annotations within this file are based on VEP104.2 . VEP outputs can be converted using the `convert_vep_to_tsv_capice.sh` script in `scripts`.

The following flags are optional:
- -o / --output: The path to the directory, output filename or output directory and filename where the output is placed (will be made if it does not exists). If only a filename is supplied, or no output is supplied, the file will be placed within the input directory. __The file will always be gzipped with a .gz extension!__

_For instance:_

`-i input.txt` becomes `input_capice.txt.gz`

`-i input.txt -o output.txt` becomes `output.txt.gz`

`-i input.txt -o path/to/output.txt` becomes `path/to/output.txt.gz`

`-i input.txt -o path/to/output` becomes `path/to/output/input_capice.txt.gz`

- -c / --config: Set the location of a custom config file similar to `default.cfg` in the project root folder.
- -v / --verbose: Display more in depth messages within the progress of CAPICE.
- -vv / --debug: Display more in depth and debug messages within the progress of CAPICE.
- -f / --force: Overwrite an output file if already present (does NOT work for logfiles).
- --train: Activates the 'train new CAPICE-like models' within CAPICE.

_Alternatively, further setup can be performed in the `default.cfg`_

#### Output of CAPICE prediction files

A file will be put out containing the following columns:

- chr_pos_ref_alt: column containing the chromosome, position, reference and alternative separated by an underscore.
- GeneName: The ENSEMBL gene name of the variant as supplied by VEP.
- FeatureID: The ENSEMBL feature ID (Transcript ID or regulatory feature ID).
- Consequence: The type of consequence that the variant has as supplied by VEP.
- probabilities: The predicted CAPICE score for the variant. The higher the score, the more likely that the variant is pathogenic.

### Usage for making new CAPICE like models

Outside of Predictions, this repository also provides users the availability to create new CAPICE like models according to their specific use case.
Unlike CAPICE Predictions, this input file is fully dependent on the imputing file used to impute the input dataset, but requires 2 columns at the very least: `sample_weight` and `binarized_label`.
Sample weight can be 1 for all samples if no sample weight should be applied. Binarized label should be either 0 or 1, depending on your labels of classification. 
_Note: when applying balancing to the input dataset, only a 2 class problem can be processed._

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
with open(path/to/model_file.pickle.dat, 'rb') as model_file:
    model = pickle.load(model_file)
```

## FAQ:

- Will CAPICE support CADD 1.6 and Genome Build 38?

While genome build 38 will be supported in the future, CADD 1.6 will not be. Even CADD 1.4 is deprecated at this point. Input annotation is fully handled by VEP.

- These scores are nice and all, but what do they really mean for this particular variant?

CAPICE bases it's scoring on the training that it was provided with. A score is assigned based on features the model learned to recognize during training.
There are plans to make a "Capice Explain Tool" which will tell how a score came to be.

- Training a new model failed with an error in `joblib.externals.loky.process_executor.RemoteTraceback` with `ValueError: unknown format is not supported`. Why?

This could possibly originate from a low sample size during the cross validation in RandomSearchCV. Please [contact us](https://github.com/molgenis/capice/issues) for further help.

- I'm on Windows and installing XGBoost fails with the PIP error `“No files/directories in C:\path\to\xgboost\pip-egg-info (from PKG-INFO)”`. Am I doing something wrong?

Unfortunatly, XGBoost does not cooperate well with Windows. You might want to try to install [Setuptools](https://pypi.org/project/setuptools/) before you attempt to install the dependencies. 
If that does not work either, we suggest you use either a Unix style virtual machine or, if you are using Windows 10, the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) is also available in the Windows Store for free, which is guaranteed to work.

- I'm getting a `AttributeError: Can't get attribute 'XGBoostLabelEncoder' on <module 'xgboost.compat' from 'capice/venv/lib/python(version)/site-packages/xgboost/compat.py'>` when loading in the model, what is going wrong?

CAPICE has been further developed on Python3.8 and Python3.9, where installing xgboost 0.72.1 was unavailable other than forcing it. To fix this issue, XGBoost 0.90 can be used which is compatible with Python3.7, 3.8 and 3.9.


- I'm trying to run CAPICE, but I'm getting the following error: 
`xgboost.core.XGBoostError: XGBoost Library (libxgboost.dylib) could not be loaded.`

This error is caused on (likely) OSX when the package "OpenMP" is not installed. Please install `libomp` to get XGBoost running.

- I'm getting the following error: `ModuleNotFoundError: No module named 'sklearn'`, what is going wrong?

"sklearn" is a module that should be installed when `scikit-learn` is installed. Either install `sklearn` manually though `pip install sklearn` or try to re-install scikit-learn.

- I'm trying to run the tests, but either no tests are run or tests are throwing errors. Is this bad design?

Not at all, the tests cover at least 80% of all code of CAPICE, although specific test command is required:
```
python3 -m unittest discover src.test.python
```


