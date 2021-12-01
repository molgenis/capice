#!/bin/bash

# Stops script if any error occurs.
set -e

# Defines error echo.
errcho() { echo "$@" 1>&2; }

# Usage.
readonly USAGE="VEP VCF output to CAPICE TSV converter
Usage:
convert_vep_to_tsv_capice.sh -i <arg> -o <arg>
-i    required: The VEP output VCF
-o    required: The directory and output filename for the CAPICE .tsv.gz

Example:
bash convert_vep_vcf_to_tsv_capice.sh -i vep_out.vcf -o capice_in.tsv.gz

Requirements:
BCFTools
"

main() {
  digestCommandLine "$@"
  processFile
}

digestCommandLine() {
  while getopts i:o:h flag
  do
    case "${flag}" in
      i) input=${OPTARG};;
      o) output=${OPTARG};;
      h)
        echo "${USAGE}"
        exit;;
      \?)
        errcho "Error: invalid option"
        echo "${USAGE}"
        exit 1;;
    esac
  done

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
        valid_command_line=false
        errcho "output file already exists"
      fi
    fi
  fi

  # If a the command line arguments are invalid, exits with code 1.
  if [[ "${valid_command_line}" == false ]]; then errcho "Exiting."; exit 1; fi
}

processFile() {
  local output="${output%.gz}" # Strips '.gz' to better work with code below.
  local output_tmp="${output}.tmp"

  local -r pre_header="%CHROM\t%POS\t%REF\t%ALT\t%Consequence\t%SYMBOL\t%SYMBOL_SOURCE\t%HGNC_ID\t%Feature\t%cDNA_position\t%CDS_position\t%Protein_position\t%Amino_acids\t%STRAND\t%SIFT\t%PolyPhen\t%DOMAINS\t%MOTIF_NAME\t%HIGH_INF_POS\t%MOTIF_SCORE_CHANGE\t%EXON\t%INTRON"

  local format="${pre_header}\n"

  local args=()
  args+=("+split-vep")
  args+=("-d")
  args+=("-f" "${format}")
  args+=("-o" "${output_tmp}")
  args+=("${input}")

  echo "Starting BCFTools."

  bcftools "${args[@]}"

  echo "BCFTools finished, building output file."

  echo -e "${pre_header}" | cat - "${output_tmp}" > "${output}" && rm "${output_tmp}"

  echo "Output file ready, gzipping."

  gzip "${output}"

  echo "Done."
}

main "$@"
