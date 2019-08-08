#!/usr/bin/env bash
# Test preparation and training on a very small corpus
# To be run from repo root

# set -ev

INPUT=$1
STORAGE=${2:="/storage/"}
EPOCHS=${3:="100"}
ACCESS_KEY=$4
SECRET_KEY=$5

echo "Input directory: $INPUT"
echo "Storage directory: $STORAGE"
echo "EPOCHS: $EPOCHS"

python prepare.py -i $INPUT -s $STORAGE -key $ACCESS_KEY -secret $SECRET_KEY

sp-train \
    $STORAGE$INPUT/ \
    $STORAGE$INPUT/sp-text.txt \
    $STORAGE$INPUT/sp-model \
    --vocab-size 13317

sp-encode \
    $STORAGE$INPUT/ \
    $STORAGE$INPUT/sp-model.model \
    $STORAGE$INPUT-encoded

gpt-2 \
    $STORAGE$INPUT/dist/ \
    $STORAGE$INPUT-encoded/ \
    $STORAGE$INPUT/sp-model.model \
    --batch-size 2 \
    --g-accum-gradients 2 \
    --n-ctx 1024 \
    --n-embed 768 \
    --n-hidden 96 \
    --n-head 12 \
    --n-layer 10 \
    --log-every 2 \
    --save-every 50 \
    --validate-every 100 \
    --clean
    --epochs $EPOCHS \
    --clean

python upload.py -i $INPUT -s $STORAGE -key $ACCESS_KEY -secret $SECRET_KEY
