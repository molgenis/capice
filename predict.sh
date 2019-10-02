#!/usr/bin/env bash

cadd_annotated_path=$1
model_path=$2
prediction_savepath=$3
log_path=$4

python /groups/umcg-gcc/tmp04/umcg-sli/variant_prioritization/model_inference_tool/commands_scripts/model_inference.py \
--input_path $cadd_annotated_path \
--model_path $model_path \
--prediction_savepath $prediction_savepath \
--log_path $log_path
