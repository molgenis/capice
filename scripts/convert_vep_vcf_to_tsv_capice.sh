#!/bin/bash

# Stops script if any error occurs.
set -e

# Defines error echo.
errcho() { echo "$@" 1>&2; }

# Usage.
readonly USAGE="VEP VCF output to CAPICE TSV converter
Usage:
convert_vep_to_tsv_capice.sh -p <arg> -i <arg> -o <arg> [-b <arg>] [-t] [-f]
-p    required: The path to the BCFTools image. (available at: https://download.molgeniscloud.org/downloads/vip/images/bcftools-1.14.sif)
-i    required: The VEP output VCF.
-o    required: The directory and output filename for the CAPICE .tsv.gz.
-b    optional: The apptainer/singularity additional --bind path(s).
-f    optional: enable force.
-t    optional: enable train. Adds the ID column to the output.

Example:
bash convert_vep_vcf_to_tsv_capice.sh -p /path/to/bcftools.sif -i vep_out.vcf.gz -o capice_in.tsv.gz

Requirements:
- Apptainer (although Singularity should work too, please change the script and adjust apptainer to singularity)
- BCFTools image. (available at: https://download.molgeniscloud.org/downloads/vip/images/bcftools-1.14.sif)

Notes:
In case you have specific binds in order for your image to work, adjust this script at the commented out bind flag.
"

# Global variables
FORCE=false
TRAIN=false


main() {
  digestCommandLine "$@"
  processFile
}

digestCommandLine() {
  while getopts p:i:o:b:hft flag
  do
    case "${flag}" in
      p) bcftools_path=${OPTARG};;
      i) input=${OPTARG};;
      o) output=${OPTARG};;
      b) bind=${OPTARG};;
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

  if [ -z "${bind}" ]
  then
    bind=false
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
  local output="${output%.gz}" # Strips '.gz' to better work with code below.
  local output_tmp="${output}.tmp"

  local args=()
  args+=("exec")
  if [[ ! "${bind}" == false ]]
  then
    args+=("--bind" "${bind}")
  fi
  args+=("${bcftools_path}")
  args+=("bcftools")
  args+=("+split-vep")
  args+=("-d")
  args+=("-f" "${FORMAT}")
  args+=("-A" "tab")
  args+=("-o" "${output_tmp}")
  args+=("${input}")

  echo "Starting BCFTools."

  apptainer "${args[@]}"

  echo "BCFTools finished, building output file."

  local header_args=()
  header_args+=("exec")
  if [[ ! "${bind}" == false ]]
  then
    header_args+=("--bind" "${bind}")
  fi
  header_args+=("${bcftools_path}")
  header_args+=("bcftools")
  header_args+=("+split-vep")
  header_args+=("-l" "${input}")
  header_args+=("|" "cut" "-f" "2")
  header_args+=("|" "tr" "\n" "\t")
  header_args+=("|" "sed" "s/\t$//")

  echo -e "${HEADER}$(apptainer "${header_args[@]}" | cat - "${output_tmp}" > "${output}" && rm "${output_tmp}"

  echo "Output file ready, gzipping."

  gzip "${output}"

  echo "Done."
}

main "$@"
