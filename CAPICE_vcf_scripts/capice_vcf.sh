#!/bin/bash
#SBATCH --job-name=rd_variants
#SBATCH --output=logs/rd_variants.out
#SBATCH --error=logs/rd_variants.err
#SBATCH --time=02:30:00
#SBATCH --cpus-per-task=3
#SBATCH --mem=2gb
#SBATCH --nodes=1
#SBATCH --export=NONE
#SBATCH --get-user-env=L60

while getopts 'j:i:df' arg
do
  case ${arg} in
    i) input=${OPTARG};;
    j) id=${OPTARG};;
    f) force=true;;
    d) debug=true;;
    *) return 1 # illegal option
  esac
done

if [ -z "$input" ]
then
  echo "input file (-i) is empty"
  exit 1
fi
if [ -z "$id" ]
then
  echo "Job ID (-j) is empty"
  exit 1
fi

if [ -d "$id" ]
then
  if [ -z "$force" ]
	then
    echo "Output directory ${id} already exists, use -f to overwrite existing data."
    exit 1
	else
	  echo "Output directory ${id} already exists, -f active, overwriting..."
		rm -R ${id}/log
    rm -R ${id}/tmp
    mkdir ${id}/log
    mkdir ${id}/tmp
	fi
else
  mkdir ${id}
  mkdir ${id}/log
  mkdir ${id}/tmp
fi

if [[ $# -eq 0 ]] ; then
  echo 'example usage: capice_vcf.sh -j jobID -i path/gzipped/input/vcf/file -f -d'
  echo '-i <arg> Input Gzipped VCF file.'
  echo '-j <arg> JobID also used as name for the output directory.'
  echo '-f Override the output if it already exists.'
  echo '-d Enable debug mode (additional logging and keep intermediate files).'
  exit 0
fi



echo "  executing cadd ..."
ml CADD &> $id/log/moduleload.log
START_TIME=$SECONDS
# strip headers from input vcf for cadd
gunzip -c $input | sed '/^#/d' | bgzip > ${id}/tmp/${id}_headerless.vcf.gz
CADD.sh -a -g GRCh37 -o ${id}/tmp/cadd.tsv.gz ${id}/tmp/${id}_headerless.vcf.gz &> $id/log/CADD.log

if [ $? -eq 0 ]
then
  ELAPSED_TIME=$(($SECONDS - $START_TIME))
  echo "  done in ${ELAPSED_TIME}s"
else
  echo "  error!"
  exit 1
fi

echo "  executing capice ..."
START_TIME=$SECONDS
ml CAPICE/v1.0-foss-2018b &> $id/log/moduleload.log
ml PythonPlus/3.7.4-foss-2018b-v20.02.2 &> $id/log/moduleload.log

python ${EBROOTCAPICE}/CAPICE_scripts/model_inference.py \
--input_path ${id}/tmp/cadd.tsv.gz \
--model_path ${EBROOTCAPICE}/CAPICE_model/xgb_booster.pickle.dat \
--prediction_savepath $id/tmp/capice.tsv \
--log_path $id/log/capice.txt &> $id/log/capice.log

if [ $? -eq 0 ]
then
  ELAPSED_TIME=$(($SECONDS - $START_TIME))
  echo "  done in ${ELAPSED_TIME}s"
else
  echo "  error!"
  exit 1
fi

echo "  executing capice output to vcf mapper ..."
START_TIME=$SECONDS
ml Java
java -Djava.io.tmpdir="${TMPDIR}" -XX:ParallelGCThreads=2 -Xmx1g -jar capice2vcf.jar -i $id/tmp/capice.tsv -o $id/tmp/capice.vcf.gz  -f -t $id/tmp/ &> ${id}/log/mapper.log
if [ $? -eq 0 ]
then
  ELAPSED_TIME=$(($SECONDS - $START_TIME))
  echo "  done in ${ELAPSED_TIME}s"
else
  echo "  error!"
  exit 1
fi

echo "  executing vcfanno ..."
START_TIME=$SECONDS
ml vcfanno &> $id/log/moduleload.log
#inject location of the capice2vcf tool in the vcfAnno config.
sed "s/JOB_ID/${id}/g" conf.template > ${id}/tmp/conf.toml  &> ${id}/log/vcfanno.log 
vcfanno ${id}/tmp/conf.toml ${input} 2> ${id}/log/vcfanno.log | bgzip > ${id}/$id.vcf.gz
if [ $? -eq 0 ]
then
  ELAPSED_TIME=$(($SECONDS - $START_TIME))
  echo "  done in ${ELAPSED_TIME}s"
else
  echo "  error!"
  exit 1
fi

if [ -z "$debug" ]
then
  echo "  cleaning up ..."
	rm -R $id/tmp
	rm -R $id/log
fi
