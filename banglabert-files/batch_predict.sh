#!/bin/bash

# misc. settings
export seed=1234

# model settings
export model_name="./outputs/train_1_model/"

# input settings
# exactly one of `dataset_dir` or the test
# dataset file needs to be provided
input_settings=(
    "--test_file dataset/report.json.csv"
    # "--dataset_dir dataset/"
#   "--dataset_dir sample_inputs/single_sequence/jsonl/"
#   "--test_file sample_inputs/single_sequence/jsonl/sample_test_without_labels.jsonl"
)

# output settings
export output_dir="outputs/"

# batch sizes
export PER_DEVICE_EVAL_BATCH_SIZE=8

# optional_arguments
optional_arguments=(
    "--cache_dir cache_dir/"
    "--overwrite_cache"
)

# optional for logging
# export WANDB_PROJECT="Sequence_classification_finetuning"
# export WANDB_WATCH=false
# export WANDB_MODE="dryrun"
export WANDB_DISABLED=true


#   --------------------------------------
#   CUSTOM
#   added by Ataf
#   --------------------------------------

directory=$1

for each_csv in $directory/*.csv; do
# for each in `find $data_dir -type f`;
# do
    echo $each_csv
    python ./sequence_classification.py \
        --model_name_or_path $model_name \
        --output_dir $output_dir \
        --per_device_eval_batch_size=$PER_DEVICE_EVAL_BATCH_SIZE \
        --seed $seed --overwrite_output_dir  --do_predict \
        --test_file $each_csv \
        # $(echo ${optional_arguments[@]})
done 


