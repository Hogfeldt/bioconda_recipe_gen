#!/bin/bash
echo "Hello from test script"
bioconda-recipe-gen ./bioconda-recipes -n kallisto2 -u https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz --tests ./travis/data/kallisto -s b32c74cdc0349c2fe0847b3464a3698da89212a507332a06291b6fc27b4e2305 -v 0.45.0 --debug --commands "kallisto version"

