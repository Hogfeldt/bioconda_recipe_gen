#!/bin/bash
##### Constants

BR_PATH=./bioconda-recipes
DATA_PATH=./travis/data

##### functions

build_kallisto()
{
    name=kallisto2
    url=https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz
    sha=b32c74cdc0349c2fe0847b3464a3698da89212a507332a06291b6fc27b4e2305
    tests=$DATA_PATH/kallisto
    version=0.45.0
    commands="kallisto version"
    bioconda-recipe-gen $BR_PATH -n $name -u $url --tests $tests -s $sha -v $version --debug --commands $commands
}

build_htstream()
{
    name=htstream2
    url=https://github.com/ibest/HTStream/archive/v1.0.0-release.tar.gz
    sha=4cf9ea61be427ea71c346e438ad2871cf0c7671948819647ef8f182d54e955fe
    version=1.0.1
    commands="hts_Stats --help" "hts_AdapterTrimmer --help" "hts_CutTrim --help" "hts_NTrimmer --help" "hts_Overlapper --help" "hts_PolyATTrim --help" "hts_QWindowTrim --help" "hts_SeqScreener --help" "hts_SuperDeduper --help"
    patches=$DATA_PATH/htstream
    bioconda-recipe-gen $BR_PATH -n $name -u $url -s $sha -v $version --test-commands $commands --patches $patches
}

build_qfilt()
{
    name=qfilt2
    url=https://github.com/veg/qfilt/archive/0.0.1.tar.gz
    sha=b0ada01c44c98b1a8bebf88c72a845b24f91a7cc63687e228b1ad872681adc09
    version=0.0.1
    commands="qfilt -h 2>&1 | grep 'filter sequencing data using some simple heuristics' > /dev/null"
    bioconda-recipe-gen $BR_PATH -n $name -u $url -s $sha -v $version --test-commands "$commands"
}

build_libdivsufsort()
{
    name=libdivsufsort2
    url=https://github.com/y-256/libdivsufsort/archive/5f60d6f026c30fb4ac296f696b3c8b0eb71bd428.tar.gz
    md5=209482686af0b9283659637bd6d51297
    version=2.0.2
    commands="test -e ${PREFIX}/include/divsufsort.h" "test -e ${PREFIX}/include/divsufsort64.h"
    bioconda-recipe-gen $BR_PATH -n $name -u $url -m $md5 -v $version --test-commands $commands
}

build_tn93()
{
    name=tn932
    url=https://github.com/veg/tn93/archive/v1.0.6.tar.gz
    sha=f7a9d03a6bd36c8507ed7630693e94d8507ed30f51b325df02ab2ea1726326e4
    version=1.0.6
    commands="tn93 -h 2>&1 | grep 'usage'"
    bioconda-recipe-gen $BR_PATH -n $name -u $url -s $sha -v $version --test-commands "$commands"
}

##### Choose package to build

package=$1
case $package in
    # Cmake and Make packages
    kallisto)           build_kallisto;;
    htstream)           build_htstream;;
    qfilt)              build_qfilt;;
    libdivsufsort)      build_libdivsufsort;;
    tn93)               build_tn93;;
esac
