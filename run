#!/bin/bash

T="$(date +%s)"
subreddit=$1
sample=$2

handle_error() {
    local exit_code=$?
    echo "An error occurred with exit code $exit_code"
    exit $exit_code
}

trap 'handle_error' ERR

python3 generate.py $subreddit
python3 combine.py $sample

T="$(($(date +%s)-T))"
echo "Done in ${T} seconds"
