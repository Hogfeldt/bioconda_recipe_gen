#!/bin/bash
##### Constants
# The TRAVIS_BUILD_DIR is specified by travis itself
DATA_PATH=$TRAVIS_BUILD_DIR/travis/data

##### functions

build_htstream()
{
    data=$DATA_PATH/htstream
    bioconda-recipe-gen build $data cmake
}

build_qfilt()
{
    data=$DATA_PATH/qfilt
    bioconda-recipe-gen build $data cmake
}

build_libdivsufsort()
{
    data=$DATA_PATH/libdivsufsort
    bioconda-recipe-gen build $data cmake
}

build_lambda()
{
    data=$DATA_PATH/lambda
    bioconda-recipe-gen build $data cmake
}

build_fuma()
{
    data=$DATA_PATH/fuma
    yes | bioconda-recipe-gen build $data python2
}

build_crossmap()
{
    data=$DATA_PATH/crossmap
    yes | bioconda-recipe-gen build $data python3
}


##### Choose package to build
package=$1
case $package in
    # Cmake and Make packages
    htstream)           build_htstream;;
    qfilt)              build_qfilt;;
    libdivsufsort)      build_libdivsufsort;;
    lambda)             build_lambda;;
    fuma)               build_fuma;;
    crossmap)           build_crossmap;;
esac
