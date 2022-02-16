# CAPICE : a computational method for Consequence-Agnostic Pathogenicity Interpretation of Clinical Exome variations
CAPICE is a computational method for predicting the pathogenicity of SNVs and InDels. It is a gradient boosting tree
model trained using a variety of genomic annotations used by CADD score and trained on the clinical significance. CAPICE
performs consistently across diverse independent synthetic, and real clinical data sets. It ourperforms the current best
method in pathogenicity estimation for variants of different molecular consequences and allele frequency.

The software can be used as web service, as pre-computed scores or by installing the software locally, all described
below.

## Use online web service
CAPICE can be used as online service at http://molgenis.org/capice

## Requirements
* VEP v105
  * Including plugin(s):
  * [SpliceAI](https://m.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#spliceai)
* BCF tools v1.14-1
* Python >=3.8

## Install
The CAPICE software is also provided in this repository for running CAPICE in your own environment. The following
sections will guide you through the steps needed for the variant annotation and the execution of making predictions
using the CAPICE model.

### UNIX like systems
__Note: performance of CAPICE has been tested on Python 3.8, 3.9 and 3.10. Performance on other Python versions is not
guaranteed.__

1. Download and installation

_Preffered_

```commandline
pip install capice
```

_Optional_

```commandline
git clone https://github.com/molgenis/capice.git
cd capice
pip install .
```

### Windows
__Installation on Windows systems is as of current not possible. Please refer to UNIX like systems (iOS or Linux) or use
the [Windows subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 
You may also use the Singularity image of CAPICE found [here](https://download.molgeniscloud.org/downloads/vip/images/).__

### SpliceAI
CAPICE requires additional VEP plugin [SpliceAI](https://m.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#spliceai). 
Files for SpliceAI can be found [here] after creating an account (for free). 
In order to obtain the SNV and Indel files you must apply for the `Predicting splicing from primary sequence` project (should be free).
The link to apply can be found within the VEP [SpliceAI](https://m.ensembl.org/info/docs/tools/vep/script/vep_plugins.html#spliceai) plugin description.
The files can then be found within the `Predicting splicing from primary sequence` project -> ANALYSES -> genome_scores_v`X` -> FILES -> genome_scores_v`X` (where `X` is the latest version). 

## Usage
### VEP
In order to score your variants through CAPICE, you have to annotate your variants using VEP by using the following
command:

```commandline
vep --input_file <path to your input file> --format vcf --output_file <path to your output file> --vcf 
--compress_output gzip --regulatory --sift s --polyphen s --domains --numbers --symbol --shift_3prime 1 
--allele_number --no_stats --offline --cache --dir_cache </path/to/cache/105> --species "homo_sapiens" 
--assembly <GRCh37 or GRCh38> --refseq --use_given_ref --exclude_predicted --use_given_ref --flag_pick_allele --force_overwrite 
--fork 4 --af_gnomad --pubmed --dont_skip --allow_non_variant
```

Then you have to convert the VEP output to TSV using our own BCFTools script: 
`/scripts/convert_vep_vcf_to_tsv_capice.sh -i */path/to/vep_output.vcf.gz* -o */path/to/capice_input.tsv.gz*`

### CAPICE
CAPICE can be run by using the following command:

`capice [-h] [-v] [--version] {module}` _arguments_

- `-h`: Print help and exit.
- `-v`: Verbose flag. Add multiple `v` to increase verbosity (more than 2 `v` does not further increase verbosity).
- `--version`: Print current CAPICE version and exit.

CAPICE currently has 2 available modules:

- `predict`
- `train`

For both module `predict` and `train`, the following arguments are available:

- -i / --input **(required)**: The path to the
  input [VEP annotated](https://www.ensembl.org/info/docs/tools/vep/index.html) dataset using the tab separator (can be
  both gzipped or not). An example of an input TSV file can be found in `CAPICE_example/CAPICE_input.tsv.gz` for genome
  build 37. The annotations within this file are based on VEP105 . VEP outputs can be converted using
  the `convert_vep_to_tsv_capice.sh` script in `scripts` using BCFTools.
- -o / --output _(optional)_: The path to the directory, output filename or output directory and filename where the
  output is placed (will be made if it does not exists). If only a filename is supplied, or no output is supplied, the
  file will be placed within the directory of which CAPICE was called from. __The file will always be gzipped with a .gz
  extension!__

_For instance:_

`-i input.tsv` becomes `input_capice.tsv.gz`

`-i input.tsv -o output.txt` becomes `output.txt.gz`

`-i input.tsv -o path/to/output.tsv` becomes `path/to/output.tsv.gz`

`-i input.tsv -o path/to/output` becomes `path/to/output/input_capice.tsv.gz`

- -f / --force: Overwrite an output file if already present (does NOT work for logfiles).

The following argument is specific to `predict`:

- -m / --model **(required)**: The path to a custom pickled CAPICE model that includes
  attributes `CAPICE_version` (`str`) and `impute_values` (`dict`). Models can be found within the `CAPICE_model`
  directory.

The following arguments are specific to `train`:

- -m / --impute **(required)**: The path to a JSON containing the impute values with the column name as key and the
  impute value as value.
  **Please note that CAPICE is value type specific!**
- -s / --split _(optional)_: Percentage of input data that should be used to measure performance during training.
  Argument should be given in float from 0.1 (10%) to 0.9 (90%), default = 0.2.

You can also use `capice {module} --help` to show help on the command line.

#### Output of CAPICE prediction files
A file will be put out containing the following columns:

- chr: column containing the chromosome of a variant
- pos: the position of the variant
- ref: the reference of the variant
- alt: the alternative of the variant
- gene_name: The gene name of the variant as supplied.
- gene_id: The id of the gene name.
- id_source: The source of the gene id.
- transcript: The transcript of the variant as supplied.
- score: The predicted CAPICE score for the variant. The higher the score, the more likely that the variant is
  pathogenic.
- suggested_class: __Suggested__ output class of the variant keeping in mind the score and gene. 
Currently VUS only. Work in progress.

### Usage for making new CAPICE like models
Outside of Predictions, this repository also provides users the availability to create new CAPICE like models according
to their specific use case. Since the input file features are not validated apart from 6 features (`%CHROM`, `%POS`
, `%REF`, `%ALT`, `%sample_weight`, `%binarized_label` (case sensitive, `%` or `#` optional)), user can provide their
own features. Please note that performance is validated on natively supported features. **Performance is not guaranteed
for custom features.**
Sample weight can be 1 for all samples if no sample weight should be applied. Binarized label should be either 0 or 1,
depending on your labels of classification. Train is optimized for a 2 class problem, performance is not guaranteed for
more than 2 classes.

#### Outputs for training a new model:
A file will be put out containing the following element:

- `xgb_classifier`: Custom [Pickled](https://docs.python.org/3/library/pickle.html) instance of
  a [XGBClassifier](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier) instance that
  has successfully trained on the input data, containing additional attributes CAPICE_version and impute_values.

_Note: to load in a pickled instance of a model, use the following commands:_

```
import pickle
with open(path/to/model_file.pickle.dat, 'rb') as model_file:
    model = pickle.load(model_file)
```

## FAQ:
- Will CAPICE support CADD 1.6 and Genome Build 38?

No. CADD has moved on to Snakemake and is quite slow. It also limits us on updating VEP for improved and bugfixes on
features. However, CAPICE will support genome build 38.

- These scores are nice and all, but what do they really mean for this particular variant?

CAPICE bases it's scoring on the training that it was provided with. A score is assigned based on features the model
learned to recognize during training. There are plans to make a "Capice Explain Tool" which will tell how a score came
to be.

- Training a new model failed with an error in `joblib.externals.loky.process_executor.RemoteTraceback`
  with `ValueError: unknown format is not supported`. Why?

This could possibly originate from a low sample size during the cross validation in RandomSearchCV.
Please [contact us](https://github.com/molgenis/capice/issues) for further help.

- I'm on Windows and installing XGBoost fails with the PIP
  error `“No files/directories in C:\path\to\xgboost\pip-egg-info (from PKG-INFO)”`. Am I doing something wrong?

Unfortunatly, XGBoost does not cooperate well with Windows. You might want to try to
install [Setuptools](https://pypi.org/project/setuptools/) before you attempt to install the dependencies. If that does
not work either, we suggest you use either a Unix style virtual machine or, if you are using Windows 10,
the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) is also available in the
Windows Store for free, which is guaranteed to work.

You could also use CAPICE through the [Singularity Container](https://download.molgeniscloud.org/downloads/vip/images/).

- I'm getting
  a `AttributeError: Can't get attribute 'XGBoostLabelEncoder' on <module 'xgboost.compat' from 'capice/venv/lib/python(version)/site-packages/xgboost/compat.py'>`
  when loading in the model, what is going wrong?

CAPICE has been further developed on Python3.8 and Python3.9, where installing xgboost 0.72.1 was unavailable other than
forcing it. To fix this issue, XGBoost 0.90 can be used which is compatible with Python3.7, 3.8 and 3.9.

- I'm trying to run CAPICE, but I'm getting the following error:
  `xgboost.core.XGBoostError: XGBoost Library (libxgboost.dylib) could not be loaded.`

This error is caused on (likely) OSX when the package "OpenMP" is not installed. Please install `libomp` to get XGBoost
running.

- I'm getting the following error: `ModuleNotFoundError: No module named 'sklearn'`, what is going wrong?

"sklearn" is a module that should be installed when `scikit-learn` is installed. Either install `sklearn` manually
though `pip install sklearn` or try to re-install scikit-learn.

- I'm getting the warning `/usr/local/lib/python3.8/dist-packages/joblib/_multiprocessing_helpers.py:45: UserWarning: [Errno 2] No such file or directory.  joblib will operate in serial mode
  warnings.warn('%s.  joblib will operate in serial mode' % (e,))` when using the CAPICE Singularity image, what's wrong?

This is likely due to the fact that the Singularity image searches for shared memory, which is different for Windows style operating systems.
This means that any and all multiprocessing parts of CAPICE will perform in single threaded mode. Other than that, CAPICE should work just fine.

## Overview of code
If you're lost in the code, a map can be
found [here](https://drive.google.com/file/d/1R_yM6pZ_m2DPazBqx2KdaG9sP5ZXC2K2/view?usp=sharing).
