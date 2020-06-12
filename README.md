# CAPICE : a computational method for Consequence-Agnostic Pathogenicity Interpretation of Clinical Exome variations

CAPICE is a computational method for predicting the pathogenicity of SNVs and InDels. 
It is a gradient boosting tree model trained using a variety of genomic annotations used by 
CADD score and trained on the clinical significance. CAPICE performs consistently across diverse independent synthetic, 
and real clinical data sets. It ourperforms the current best method in pathogenicity estimation
for variants of different molecular consequences and allele frequency.

## Requirements
Python 3.6 (doesn't work with 3.7 or 3.8)

## Precomputed scores for all possible SNVs and InDels
We precomputed the CAPICE score for all possible SNVs and InDels. It can be downloaded via [zenodo](https://doi.org/10.5281/zenodo.3516248).

The file contains the following columns:
*#CHROM* chromosome name, as [1:22, X]
*POS* genomic position (GrCh37 genome assembly)
*REF* reference allele
*ALT* alternative allele
*score* CAPICE score. The score ranges from 0 to 1, the higher the more likely the variant is pathogenic


## CAPICE software
The CAPICE software is also provided in this repository for running CAPICE in your own environment. 
The following sections will guide you through the steps needed for the variant annotation and the execution of
making predictions using the CAPICE model.


## Downloads, installation and processing of the input files
### 1. Software and libraries
CAPICE scripts can be downloaded from the CAPICE github repository. The CAPICE model
can be downloaded via #tbd
```angular2
git clone https://github.com/molgenis/capice.git
cd capice
```

### 2. Variant annotation and input file format
CAPICE uses the same set of features used in [CADD](https://cadd.gs.washington.edu/). In this
repository we also provide an example input variant list in *CAPICE_example/test_input.vcf* and 
the annotated input file in *CAPICE_example/test_caddAnnotated.tsv.gz* 

### 3. Perform prediction
Once the annotated file is ready then the last step would be using the pre-trained model provided
in the github repository.
```angular2
bash predict.sh \
/path/to/input \
/path/to/CAPICE_model \
/path/to/output \
/path/to/log_file
```
The output file would contain the chromosome, position, reference and alternative allele
information of the input list of variants.
