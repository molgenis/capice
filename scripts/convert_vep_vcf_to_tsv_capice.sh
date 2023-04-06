#!/bin/bash

# Stops script if any error occurs.
set -e

# Defines error echo.
errcho() { echo "$@" 1>&2; }

# Usage.
readonly USAGE="VEP VCF output to CAPICE TSV converter
Usage:
convert_vep_to_tsv_capice.sh -p <arg> -i <arg> -o <arg> [-t] [-f]
-p    required: The path to the BCFTools image. (available at: https://download.molgeniscloud.org/downloads/vip/images/bcftools-1.14.sif)
-i    required: The VEP output VCF.
-o    required: The directory and output filename for the CAPICE .tsv.gz.
-f    optional: enable force.
-t    optional: enable train. Adds the ID column to the output.

Please note that this script expects apptainer binds to be set correctly by the system administrator.
Additional apptainer binds can be set by setting the environment variable APPTAINER_BIND.
If using SLURM, please export this environment variable to the sbatch instance too.

Example:
bash convert_vep_vcf_to_tsv_capice.sh -p /path/to/bcftools.sif -i vep_out.vcf.gz -o capice_in.tsv.gz

Requirements:
- Apptainer (although Singularity should work too, please change the script and adjust apptainer to singularity)
- BCFTools image. (available at: https://download.molgeniscloud.org/downloads/vip/images/bcftools-1.14.sif)
"

# Global variables
FORCE=false
TRAIN=false


main() {
  digestCommandLine "$@"
  processFile
}

digestCommandLine() {
  while getopts p:i:o:hft flag
  do
    case "${flag}" in
      p) bcftools_path=${OPTARG};;
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
    HEADER="CHROM\tPOS\tID\tREF\tALT\t"
    FORMAT="%CHROM\t%POS\t%ID\t%REF\t%ALT\t%CSQ\n"
  else
    HEADER="CHROM\tPOS\tREF\tALT\t"
    FORMAT="%CHROM\t%POS\t%REF\t%ALT\t%CSQ\n"
  fi

  validateCommandLine
}

validateCommandLine() {
  local valid_command_line=true

  # Validate if BCFTools image is set & not empty
  if [ -z "${bcftools_path}" ]
  then
    valid_command_line=false
    errcho "BCFTools image not set/empty"
  else
    if [ ! -f "${bcftools_path}" ]
    then
      valid_command_line=false
      errcho "BCFTools image does not exist"
    fi
  fi

  # Validate if input is set & not empty.
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
  local output="${output%.gz}"

  local args=()
  args+=("exec")
  args+=("${bcftools_path}")
  args+=("bcftools")
  args+=("+split-vep")

  # Header

  echo "Obtaining header"

  header_args=("${args[@]}")
  header_args+=("-l" "${input}")

  present_features=$(apptainer "${header_args[@]}" | cut -f 2 | tr "\n" "\t" | sed "s/\t$//")

  echo -e "${HEADER}$present_features" > ${output}

  # VEP VCF file content

  echo "Obtaining VCF content"

  file_args=("${args[@]}")
  file_args+=("-d")
  file_args+=("-f" "${FORMAT}")
  file_args+=("-A" "tab")
  file_args+=("${input}")

  apptainer "${file_args[@]}" >> ${output}

  echo "BCFTools finished."

  echo "Gzipping output file."

  gzip "${output}"

  echo "Done."
}

main "$@"
