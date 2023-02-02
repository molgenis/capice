[![Build Status](https://app.travis-ci.com/molgenis/capice.svg?branch=main)](https://app.travis-ci.com/molgenis/capice)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=molgenis_capice&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=molgenis_capice)

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
The list below is a complete list. Depending on whether GRCh37 and/or GRCh38 is used and whether all
mentioned features are used, some items in the list below can be skipped.

* VEP v107
  * Including VEP cache (which needs to be unarchived!):
    * [homo_sapiens_refseq_vep_107_GRCh37](http://ftp.ensembl.org/pub/release-107/variation/indexed_vep_cache/homo_sapiens_refseq_vep_107_GRCh37.tar.gz)
    * [homo_sapiens_refseq_vep_107_GRCh38](http://ftp.ensembl.org/pub/release-107/variation/indexed_vep_cache/homo_sapiens_refseq_vep_107_GRCh38.tar.gz)
  * Including plugin(s):
    * [Grantham](https://github.com/molgenis/vip/blob/master/resources/vep/plugins/Grantham.pm)
    * [SpliceAI](https://github.com/molgenis/vip/blob/master/resources/vep/plugins/SpliceAI.pm)
  * Including additional data (GRCh37) [available here](https://download.molgeniscloud.org/downloads/vip/resources/GRCh37/):
    * `gnomad.total.r2.1.1.sites.stripped.vcf.gz`
    * `gnomad.total.r2.1.1.sites.stripped.vcf.gz.csi`
    * `hg19.100way.phyloP100way.bw`
    * `spliceai_scores.masked.indel.hg19.vcf.gz`
    * `spliceai_scores.masked.indel.hg19.vcf.gz.tbi`
    * `spliceai_scores.masked.snv.hg19.vcf.gz`
    * `spliceai_scores.masked.snv.hg19.vcf.gz.tbi` 
  * Including additional data (GRCh38) [available here](https://download.molgeniscloud.org/downloads/vip/resources/GRCh38/):
    * `gnomad.genomes.v3.1.2.sites.stripped.vcf.gz`
    * `gnomad.genomes.v3.1.2.sites.stripped.vcf.gz.csi`
    * `hg38.phyloP100way.bw`
    * `spliceai_scores.masked.indel.hg38.vcf.gz`
    * `spliceai_scores.masked.indel.hg38.vcf.gz.tbi`
    * `spliceai_scores.masked.snv.hg38.vcf.gz`
    * `spliceai_scores.masked.snv.hg38.vcf.gz.tbi` 
* Apptainer == 1.1.* (For: [BCFTools singularity image](https://download.molgeniscloud.org/downloads/vip/images/bcftools-1.14.sif)).
  * Singularity could also work, but requires manual adjusting of [the conversion script](./scripts/convert_vep_vcf_to_tsv_capice.sh).
* Python >=3.10

## Install
The CAPICE software is also provided in this repository for running CAPICE in your own environment. The following
sections will guide you through the steps needed for the variant annotation and the execution of making predictions
using the CAPICE model.

### UNIX like systems
__Note: performance of CAPICE has been tested on Python 3.10. Performance on other Python versions is not
guaranteed.__

1. Download and installation

_Preferred_

```commandline
pip install capice
```

_Optional_

```commandline
git clone https://github.com/molgenis/capice.git
cd capice
pip install .
```

_Developers_
```commandline
git clone https://github.com/molgenis/capice.git
cd capice
pip install -e '.[test]'
```

Additionally, the [BCFTools Singularity image](https://download.molgeniscloud.org/downloads/vip/images/bcftools-1.14.sif) has to be obtained.

### Windows
__Installation on Windows systems is as of current not possible. Please refer to UNIX like systems (macOS or Linux) or use
the [Windows subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 
You may also use the Singularity image of CAPICE found [here](https://download.molgeniscloud.org/downloads/vip/images/).__

### Singularity
Singularity images of CAPICE are made available as part of the VIP pipeline. These can be found [here](https://download.molgeniscloud.org/downloads/vip/images/).

## Usage
### VEP
In order to score your variants through CAPICE, you have to annotate your variants using VEP by using the following
command:

```commandline
vep --input_file <path to your input file> --format vcf --output_file <path to your output file> \
--vcf --compress_output gzip --sift s --polyphen s --numbers --symbol \
--shift_3prime 1 --allele_number --refseq --total_length --no_stats --offline --cache \
--dir_cache </path/to/cache/107> --species "homo_sapiens" --assembly <GRCh37 or GRCh38> \
--fork <n_threads> --dont_skip --allow_non_variant --use_given_ref --exclude_predicted \
--flag_pick_allele --plugin Grantham \
--plugin SpliceAI,snv=<path/to/spliceai_scores.masked.snv.vcf.gz>,indel=</path/to/spliceai_scores.masked.indel.vcf.gz> \
--custom "<path/to/gnomad.total.sites.stripped.vcf.gz>,gnomAD,vcf,exact,0,AF,HN" \
--custom "<path/to/phyloP100way.bw>,phyloP,bigwig,exact,0" \
--dir_plugins <path to your VEP plugin directory>
```
**IMPORTANT: Ensure the right files are used based on GRCH37 or GRCH38!!!**

Note: Certain arguments might not be needed if training/predicting without using all possible features offered by CAPICE.

Then you have to convert the VEP output to TSV using our own BCFTools script: 
`./scripts/convert_vep_vcf_to_tsv_capice.sh -i </path/to/vep_output.vcf.gz> -o </path/to/capice_input.tsv.gz>`

### CAPICE
CAPICE can be run by using the following command:

`capice [-h] [-v] [--version] {module}` _arguments_

- `-h`: Print help and exit.
- `-v`: Verbose flag. Add multiple `v` to increase verbosity (more than 2 `v` does not further increase verbosity).
- `--version`: Print current CAPICE version and exit.

CAPICE currently has the following available modules:

- `predict`
- `train`
- `explain`

For all modules `predict`, `train` and `explain`, the following arguments are available:

- -i / --input **(required)**: The path to the
  input [VEP annotated](https://www.ensembl.org/info/docs/tools/vep/index.html) dataset using the tab separator (can be
  both gzipped or not). Example input data can be found in the [resources](./resources) directory (based on genome build 37 with VEP105).
  The non-raw input files can be used directly with CAPICE.
  VEP outputs can be converted using `convert_vep_to_tsv_capice.sh` in the [scripts](./scripts) directory (requires apptainer).
- -o / --output _(optional)_: The path to the directory, output filename or output directory and filename where the
  output is placed (will be made if it does not exists). If only a filename is supplied, or no output is supplied, the
  file will be placed within the directory of which CAPICE was called from. __The file will always be gzipped with a .gz
  extension!__

_For instance:_

`-i input.tsv` creates the output file `input_capice.tsv.gz`

`-i input.tsv -o output.tsv.gz` creates the output file `output.tsv.gz`

`-i input.tsv -o path/to/output.tsv.gz` creates the output file `path/to/output.tsv.gz`

`-i input.tsv -o path/to/output_directory` creates the output file `path/to/output_directory/input_capice.tsv.gz`

- -f / --force: Overwrite an output file if already present.

The following argument is specific to `predict`:

- -m / --model **(required)**: The path to the (universal binary) json model that includes
  attributes `CAPICE_version` (`str`), `vep_features` (`list[str]`), `processable_features` (`list[str]`) and `predict_proba` (`XGBoost.XGBClassifier`). 
  Models can be found as attachments on the [GitHub releases](https://github.com/molgenis/capice/releases) page.

The following arguments are specific to `train`:

- -e / --features **(required)**: The path to a JSON containing the features desired for training as supplied in the input file. Each key is a training feature, each value is ignored and can be left `null`.
  **Please note that the features are case-sensitive!**
- -s / --split _(optional)_: Percentage of input data that should be used to measure performance during training.
  Argument should be given in float from 0.1 (10%) to 0.9 (90%), default = 0.2.
- -t / --threads _(optional)_: The amount of processing cores the training protocol can use. Default = 1.

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
- feature: The feature of the variant as supplied.
- feature_type: The type of the feature of the variant as supplied.
- score: The predicted CAPICE score for the variant. The higher the score, the more likely that the variant is
  pathogenic.
- suggested_class: __Suggested__ output class of the variant keeping in mind the score and gene. 
Currently VUS only. Work in progress.

### Usage for making new CAPICE like models
Outside of Predictions, this repository also provides users the availability to create new CAPICE like models according
to their specific use case. Since the input file features are not validated apart from 6 features (`CHROM`, `POS`
, `REF`, `ALT`, `sample_weight`, `binarized_label` (case sensitive)), user can provide their
own features. Please note that performance is validated on natively supported features. **Performance is not guaranteed
for custom features.**
Sample weight can be 1 for all samples if no sample weight should be applied. Binarized label should be either 0 or 1,
depending on your labels of classification. Train is optimized for a 2 class problem. Performance is not guaranteed for
more than 2 classes.

#### Outputs for training a new model:
A file will be put out containing the following element:

- `xgb_classifier`: [Universal Binary Json](https://ubjson.org/) or JSON file of
  a [XGBClassifier](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier) instance that
  has successfully trained on the input data, containing additional attributes CAPICE_version, vep_features and processable_features.

_Note: To load in the (universal binary) json model, use the following commands:_

```python
import xgboost as xgb
model = xgb.XGBClassifier()
model.load_model('/path/to/model.ubj')
```

### Usage for the explain module
__Is only supported for CAPICE models that have been created using CAPICE v5.0.0 or greater!__

The explain module takes a model and exports the feature importances of said model. 
Each of the importance type is described [here](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.Booster.get_score).

Do note that the output of the explain module will always a gzipped TSV, just like the output of `predict`.

## FAQ:
__Question:__  
Will CAPICE support CADD 1.6 and Genome Build 38?

__Answer:__  
No (CADD 1.6) and yes (Genome Build 38). CADD has moved on to Snakemake and is quite slow.
It also limits us on updating VEP for improved and bugfixes on features. However, CAPICE will support genome build 38.

---

__Question:__  
These scores are nice and all, but what do they really mean for this particular variant?

__Answer:__  
CAPICE bases it's scoring on the training that it was provided with. A score is assigned based on features the model
learned to recognize during training. There are plans to make a "Capice Explain Tool" which will tell how a score came
to be.

---

__Question:__   
Training a new model failed with an error in `joblib.externals.loky.process_executor.RemoteTraceback`
  with `ValueError: unknown format is not supported`. Why?

__Answer:__  
This could possibly originate from a low sample size during the cross validation in RandomSearchCV.
Please [contact us](https://github.com/molgenis/capice/issues) for further help.

---

__Question:__  
I'm on Windows and installing XGBoost fails with the PIP
  error `“No files/directories in C:\path\to\xgboost\pip-egg-info (from PKG-INFO)”`. Am I doing something wrong?

__Answer:__  
Unfortunately, XGBoost does not cooperate well with Windows. You might want to try to
install [Setuptools](https://pypi.org/project/setuptools/) before you attempt to install the dependencies. If that does
not work either, we suggest you use either a Unix style virtual machine or, if you are using Windows 10,
the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) is also available in the
Windows Store for free, which is guaranteed to work.

You could also use CAPICE through the [Singularity Container](https://download.molgeniscloud.org/downloads/vip/images/).

---

__Question:__  
I'm trying to run CAPICE, but I'm getting the following error:
  `xgboost.core.XGBoostError: XGBoost Library (libxgboost.dylib) could not be loaded.`

__Answer:__  
This error is caused on (likely) macOS when the package "OpenMP" is not installed. Please install `libomp` to get XGBoost
running.

---

__Question:__  
I'm getting the following error: `ModuleNotFoundError: No module named 'sklearn'`. What is going wrong?

__Answer:__  
`sklearn` is a module that should be installed when `scikit-learn` is installed. Either install `sklearn` manually
though `pip install sklearn` or try to re-install `scikit-learn`.

---

__Question:__  
I'm getting the warning `/usr/local/lib/python3.8/dist-packages/joblib/_multiprocessing_helpers.py:45: UserWarning: [Errno 2] No such file or directory.  joblib will operate in serial mode
  warnings.warn('%s.  joblib will operate in serial mode' % (e,))` when using the CAPICE Singularity image. What's going wrong?

__Answer:__  
This is likely due to the fact that the Singularity image searches for shared memory, which is different for Windows style operating systems.
This means that any and all multiprocessing parts of CAPICE will perform in single threaded mode. Other than that, CAPICE should work just fine.

---

__Question:__  
I want to use the [standalone SpliceAI](https://github.com/Illumina/SpliceAI) instead of the VEP plugin. Is this possible?

__Answer:__  
We are investigating options to include the standalone SpliceAI since this requires a lot less resources for the precomputed scores that the VEP plugin uses.
You could try to use it, but proceed at your own risk.

---

__Question:__  
CAPICE gives an error that the model version does not match with the CAPICE version.

__Answer:__  
There are certain restrictions regarding what model versions can be used with CAPICE.
For regular releases, the major version must be identical.
For pre-release versions (with `rc<number>` in the version), the entire version number (major, minor, patch & pre-release) must be identical.

---

__Question:__  
I created/am using a `.pickle.dat` model, but the newer versions of CAPICE switched to `.ubj`/`.json` instead for models.
Can I somehow use my old `.pickle.dat` with newer versions of CAPICE.

__Answer:__  
First of all, it's important to note that with every major release, breaking changes might be implemented.
However, it might be possible to upgrade a CAPICE 4.x.x model to a model usable by CAPICE 5.x.x (though no guarantees are
given!).

To convert a `.pickle.dat` model to `.ubj`/`.json`, one can do the following (using a local git clone of the repository):
1. Git checkout the CAPICE version (tag) on which the model was trained.
2. Create/load a virtual environment (venv) & pip install from the source code.
3. Use the following python code:
   ```python
   import sys
   import pickle

   with open(sys.argv[1], 'rb') as model_file:
       model = pickle.load(model_file)
   model.save_model(sys.argv[2])
   ```
   - `sys.argv[1]`: the input `.pickle.dat` file
   - `sys.argv[2]`: the output `.json` file
4. Adjust `CAPICE_version` within the new model file to that of the new release (major version should match!). 
   It is advisable however to ensure that the filename still contains the version it was trained on (f.e. `v4.0.0_grch37_v5.0.0-compatibility.json`) to ensure no confusion will exist on which version it was actually trained.

Do note that we recommend using a model trained on a specific major version instead, as other breaking changes might be present as well! 

## Data sources
### GnomAD
The gnomAD files can be generated through the following scripts (which also download the gnomAD files):
- GRCH37: https://github.com/molgenis/vip/blob/main/utils/create_gnomad_GRCh37.sh
- GRCH38: https://github.com/molgenis/vip/blob/main/utils/create_gnomad_GRCh38.sh

### PhyloP
PhyloP resources can be downloaded from:
- GRCh37: http://hgdownload.cse.ucsc.edu/goldenpath/hg19/phyloP100way/
- GRCh38: http://hgdownload.cse.ucsc.edu/goldenpath/hg38/phyloP100way/

### SpliceAI
Files for the SpliceAI VEP plugin can be found in the Illumina project "[Predicting splicing from primary sequence](https://basespace.illumina.com/s/5u6ThOblecrh)" (as mentioned [here](https://pypi.org/project/spliceai/)),
which can be accessed after creating an account on Illumina. Once added, the relevant files can be accessed as follows:
1. Go to the projects tab
2. Select `Predicting splicing from primary sequence`
3. Select the `analyses` subtab (might be selected by default)
4. Click on `genome_scores_v<version_number>` (select most recent version)
5. Select `files` subtab
6. Click on the `genome_scores_v<version_number>` folder
7. Select the files to download (see [Requirements](#requirements))

## Overview of code
If you're lost in the code, an outdated map can be
found [here](https://drive.google.com/file/d/1R_yM6pZ_m2DPazBqx2KdaG9sP5ZXC2K2/view?usp=sharing).
