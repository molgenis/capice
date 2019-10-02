#!/usr/bin/env bash

input_path=$1
cadd_annotated_path=$2
model_path=$3
prediction_savepath=$4
log_path=$5

CADD.sh -a -g GRCh37 -o ${cadd_annotated_path}.gz $input_path

python /groups/umcg-gcc/tmp04/umcg-sli/variant_prioritization/CLI/commands_scripts/model_inference.py \
--input_path $cadd_annotated_path \
--model_path $model_path \
--prediction_savepath $prediction_savepath \
--log_path $log_path

