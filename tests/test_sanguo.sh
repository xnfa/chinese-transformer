#!/usr/bin/env bash
# Test preparation and training on a very small corpus
# To be run from repo root

set -ev

sp-train \
    tests/sanguo/ \
    tests/sanguo/sp-text.txt \
    tests/sanguo/sp-model \
    --vocab-size 13317

sp-encode \
    tests/sanguo/ \
    tests/sanguo/sp-model.model \
    tests/sanguo-encoded

gpt-2 \
    tests/sanguo-test-run/ \
    tests/sanguo-encoded/ \
    tests/sanguo/sp-model.model \
    --batch-size 2 \
    --g-accum-gradients 2 \
    --n-ctx 1024 \
    --n-embed 768 \
    --n-hidden 96 \
    --n-head 12 \
    --n-layer 10 \
    --epochs 10 \
    --log-every 2 \
    --save-every 50 \
    --validate-every 100 \
    --clean

# resume training
gpt-2 \
    tests/sanguo-test-run/ \
    tests/sanguo-encoded/ \
    tests/sanguo/sp-model.model \
    --batch-size 8 \
    --g-accum-gradients 2 \
    --n-ctx 1024 \
    --n-embed 768 \
    --n-hidden 96 \
    --n-head 12 \
    --n-layer 10 \
    --epochs 2
