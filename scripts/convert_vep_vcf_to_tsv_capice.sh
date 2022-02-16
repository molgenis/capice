#!/bin/bash

# Stops script if any error occurs.
set -e

# Possibly variable variables
PRE_HEADER="%CHROM\t%POS\t%REF\t%ALT\t%Consequence\t%SYMBOL\t%SYMBOL_SOURCE\t%Gene\t%Feature\t%Feature_type\t%cDNA_position\t%CDS_position\t%Protein_position\t%Amino_acids\t%STRAND\t%SIFT\t%PolyPhen\t%EXON\t%INTRON\t%SpliceAI_pred_DP_AG\t%SpliceAI_pred_DP_AL\t%SpliceAI_pred_DP_DG\t%SpliceAI_pred_DP_DL\t%SpliceAI_pred_DS_AG\t%SpliceAI_pred_DS_AL\t%SpliceAI_pred_DS_DG\t%SpliceAI_pred_DS_DL"

# Defines error echo.
errcho() { echo "$@" 1>&2; }

# Usage.
readonly USAGE="VEP VCF output to CAPICE TSV converter
Usage:
convert_vep_to_tsv_capice.sh -i <arg> -o <arg>
-i    required: The VEP output VCF
-o    required: The directory and output filename for the CAPICE .tsv.gz
-f    optional: enable force
-t    optional: enable train. Adds the ID column to the output

Example:
bash convert_vep_vcf_to_tsv_capice.sh -i vep_out.vcf -o capice_in.tsv.gz

Requirements:
BCFTools
"

# Global variables
FORCE=false
TRAIN=false


main() {
  digestCommandLine "$@"
  processFile
}

digestCommandLine() {
  while getopts i:o:hft flag
  do
    case "${flag}" in
      i) input=${OPTARG};;
      o) output=${OPTARG};;
      h)
        echo "${USAGE}"
        exit;;
      t)
        TRAIN=true;;
      f)
        FORCE=true;;
      \?)
        errcho "Error: invalid option"
        echo "${USAGE}"
        exit 1;;
    esac
  done

  if [[ ${TRAIN} == true ]]
  then
    id="\t%ID"
    PRE_HEADER="$PRE_HEADER$id"
  fi

  validateCommandLine
}

validateCommandLine() {
  local valid_command_line=true

  # Validate if variable is set & not empty.
  if [ -z "${input}" ]
  then
    valid_command_line=false
    errcho "input file not set/empty"
  else
    # Validate if input file exists.
    if [ ! -f "${input}" ]
    then
      valid_command_line=false
      errcho "input file does not exist"
    else
      # Validate allowed input filetype.
      case $(file --mime-type -b "${input}") in
        text/plain);;
        application/*gzip);;
        *)
          valid_command_line=false
          errcho "input file has invalid type (plain text/gzip allowed)";;
      esac
    fi
  fi

  # Validate if variable is set & not empty.
  if [ -z "${output}" ]
  then
    valid_command_line=false
    errcho "output file not set/empty"
  else
    # Validates proper output filename.
    if [[ "${output}" != *.tsv.gz ]]
    then
      valid_command_line=false
      errcho "output filename must end with '.tsv.gz'"
    else
      # Validates if output doesn't file already exist.
      if [ -f "${output}" ]
      then
        if [[ ${FORCE} == true ]]
        then
          echo "output file exists, enforcing output"
          rm "${output}"
        else
          errcho "output file exists and force flag is not called"
          valid_command_line=false
        fi
      fi
    fi
  fi

  # If a the command line arguments are invalid, exits with code 1.
  if [[ "${valid_command_line}" == false ]]; then errcho "Exiting."; exit 1; fi
}

processFile() {
  local output="${output%.gz}" # Strips '.gz' to better work with code below.
  local output_tmp="${output}.tmp"

  local format="${PRE_HEADER}\n"

  local args=()
  args+=("+split-vep")
  args+=("-d")
  args+=("-f" "${format}")
  args+=("-o" "${output_tmp}")
  args+=("${input}")

  echo "Starting BCFTools."

  bcftools "${args[@]}"

  echo "BCFTools finished, building output file."

  echo -e "${PRE_HEADER}" | cat - "${output_tmp}" > "${output}" && rm "${output_tmp}"

  echo "Output file ready, gzipping."

  gzip "${output}"

  echo "Done."
}

main "$@"
