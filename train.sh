#!/usr/bin/env bash
# Test preparation and training on a very small corpus
# To be run from repo root

# set -ev

INPUT=$1
STORAGE=${2:="/storage/"}
EPOCHS=${3:="100"}

echo "Input directory: $INPUT"
echo "Storage directory: $STORAGE"
echo "EPOCHS: $EPOCHS"

python prepare.py -i $INPUT -s $STORAGE

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
    --epochs $EPOCHS \
    --clean

python upload.py -i $INPUT -s $STORAGE
