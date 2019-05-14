#!/bin/bash
##### Constants

BR_PATH=./bioconda-recipes
DATA_PATH=./travis/data
##### functions

build_kallisto()
{
    bioconda-recipe-gen $BR_PATH -n kallisto2 -u https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz --tests $DATA_PATH/kallisto -s b32c74cdc0349c2fe0847b3464a3698da89212a507332a06291b6fc27b4e2305 -v 0.45.0 --debug --commands "kallisto version"
}

build_htstream()
{
    bioconda-recipe-gen $BR_PATH -u https://github.com/ibest/HTStream/archive/v1.0.0-release.tar.gz -n htstream2 -s 4cf9ea61be427ea71c346e438ad2871cf0c7671948819647ef8f182d54e955fe -v 1.0.1  --test-commands "hts_Stats --help" "hts_AdapterTrimmer --help" "hts_CutTrim --help" "hts_NTrimmer --help" "hts_Overlapper --help" "hts_PolyATTrim --help" "hts_QWindowTrim --help" "hts_SeqScreener --help" "hts_SuperDeduper --help" --patches $DATA_PATH/htstream
}


##### Choose package to build

package=$1
case $package in
    # Cmake and Make packages
    kallisto)   build_kallisto;;
    htstream)   build_htstream;;
esac
