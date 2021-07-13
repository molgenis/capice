#!/bin/bash

Help()
{
  echo "VEP VCF output to CAPICE TSV converter"
  echo "Usage:"
  echo "convert_vep_to_tsv_capice.sh -i <arg> -o <arg>"
  echo -e "-i\trequired: The VEP output VCF"
  echo -e "-o\trequired: The directory and output filename for the CAPICE tsv\n"
}

main()
{
  local -r pre_header="%CHROM\t%POS\t%REF\t%ALT\t%Consequence\t%SYMBOL\t%SYMBOL_SOURCE\t%HGNC_ID\t%Feature\t%cDNA_position\t%CDS_position\t%Protein_position\t%Amino_acids\t%STRAND\t%SIFT\t%PolyPhen\t%DOMAINS\t%MOTIF_NAME\t%HIGH_INF_POS\t%MOTIF_SCORE_CHANGE\t%EXON\t%INTRON"

  local format="${pre_header}\n"

  local -r file_info="## VEP VCF to CAPICE tsv converter"

  local args=()
  args+=("+split-vep")
  args+=("-d")
  args+=("-f" "${format}")
  args+=("${input}")

  data=$(bcftools "${args[@]}")
  
  if file --mime-type "$input" | grep -q gzip$; then
	vep_line=$(zcat "${input}" | grep "VEP=")
  else
	vep_line=$(cat "${input}" | grep "VEP=")
  fi

  echo -e "${file_info}\n${vep_line}\n${pre_header}\n${data}" > ${output}

}

while getopts i:o:h flag
do
	case "${flag}" in
		i) input=${OPTARG};;
		o) output=${OPTARG};;
    h)
      Help
      exit;;
    \?)
      echo "Error: invalid option"
      exit;;
	esac
done

if [[ (-n "${input}")  &&  (-n "${output}")]]; then
  main
else
  Help
  exit
fi
