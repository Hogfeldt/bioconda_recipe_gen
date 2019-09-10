#!/bin/bash
##### Constants

BR_PATH=./bioconda-recipes
DATA_PATH=./travis/data

##### functions

build_kallisto()
{
    name=kallisto2
    url=https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz
    tests=$DATA_PATH/kallisto
    version=0.45.0
    commands="kallisto version"
    bioconda-recipe-gen $BR_PATH -n $name -u $url --tests $tests -v $version --debug --commands $commands
    status=$?
    exit $status
}

build_htstream()
{
    name=htstream2
    url=https://github.com/ibest/HTStream/archive/v1.1.0-release.tar.gz
    version=1.1.0
    commands=("hts_Stats --help" "hts_AdapterTrimmer --help" "hts_CutTrim --help" "hts_NTrimmer --help" "hts_Overlapper --help" "hts_PolyATTrim --help" "hts_QWindowTrim --help" "hts_SeqScreener --help" "hts_SuperDeduper --help")
    bioconda-recipe-gen $BR_PATH -n $name -u $url -v $version --test-commands "${commands[@]}"
}

build_clever_toolkit()
{
    name=clever-toolkit2
    url=https://bitbucket.org/tobiasmarschall/clever-toolkit/downloads/clever-toolkit-v2.4.tar.gz
    version=2.4
    commands=("clever --help > /dev/null" "laser --help > /dev/null")
    bioconda-recipe-gen $BR_PATH -n $name -u $url -v $version --test-commands "${commands[@]}"
}

build_qfilt()
{
    name=qfilt2
    url=https://github.com/veg/qfilt/archive/0.0.1.tar.gz
    version=0.0.1
    commands="qfilt -h 2>&1 | grep 'filter sequencing data using some simple heuristics' > /dev/null"
    bioconda-recipe-gen $BR_PATH -n $name -u $url -v $version --test-commands "$commands"
}

build_libdivsufsort()
{
    name=libdivsufsort2
    url=https://github.com/y-256/libdivsufsort/archive/5f60d6f026c30fb4ac296f696b3c8b0eb71bd428.tar.gz
    version=2.0.2
    commands=("test -e \${PREFIX}/include/divsufsort.h" "test -e \${PREFIX}/include/divsufsort64.h")
    cmakeflags=("DCMAKE_INSTALL_PREFIX=\$PREFIX" "DBUILD_DIVSUFSORT64=\"On\"")
    bioconda-recipe-gen $BR_PATH -n $name -u $url -v $version --test-commands "${commands[@]}" --cmake-flags "${cmakeflags[@]}"
}

build_tn93()
{
    name=tn932
    url=https://github.com/veg/tn93/archive/v1.0.6.tar.gz
    version=1.0.6
    commands="tn93 -h 2>&1 | grep 'usage'"
    bioconda-recipe-gen $BR_PATH -n $name -u $url -v $version --test-commands "$commands"
}

##### Choose package to build

package=$1
case $package in
    # Cmake and Make packages
    kallisto)           build_kallisto;;
    htstream)           build_htstream;;
    qfilt)              build_qfilt;;
    libdivsufsort)      build_libdivsufsort;;
    clever-toolkit)     build_clever_toolkit;;
    tn93)               build_tn93;;
esac
