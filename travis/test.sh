#!/bin/bash
##### Constants
# The TRAVIS_BUILD_DIR is specified by travis itself
BR_PATH=$TRAVIS_BUILD_DIR/bioconda-recipes
DATA_PATH=$TRAVIS_BUILD_DIR/travis/data

##### functions

build_kallisto()
{
    name=kallisto
    url=https://github.com/pachterlab/kallisto/archive/v0.46.2.tar.gz
    version=0.46.2
    commands="kallisto cite"
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "$commands" --template $template
}

build_htstream()
{
    name=htstream
    url=https://github.com/ibest/HTStream/archive/v1.1.0-release.tar.gz
    version=1.1.0
    commands=("hts_Stats --help" "hts_AdapterTrimmer --help" "hts_CutTrim --help" "hts_NTrimmer --help" "hts_Overlapper --help" "hts_PolyATTrim --help" "hts_QWindowTrim --help" "hts_SeqScreener --help" "hts_SuperDeduper --help")
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "${commands[@]}" --template $template -d
}

build_clever_toolkit()
{
    name=clever-toolkit
    url=https://bitbucket.org/tobiasmarschall/clever-toolkit/downloads/clever-toolkit-v2.4.tar.gz
    version=2.4
    commands=("clever --help > /dev/null" "laser --help > /dev/null")
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "${commands[@]}" --template $template
}

build_qfilt()
{
    name=qfilt
    url=https://github.com/veg/qfilt/archive/0.0.1.tar.gz
    version=0.0.1
    commands="qfilt -h 2>&1 | grep 'filter sequencing data using some simple heuristics' > /dev/null"
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "$commands" --template $template
}

build_libdivsufsort()
{
    name=libdivsufsort
    url=https://github.com/y-256/libdivsufsort/archive/5f60d6f026c30fb4ac296f696b3c8b0eb71bd428.tar.gz
    version=2.0.2
    commands=("test -e \${PREFIX}/include/divsufsort.h" "test -e \${PREFIX}/include/divsufsort64.h")
    cmakeflags=("DCMAKE_INSTALL_PREFIX=\$PREFIX" "DBUILD_DIVSUFSORT64=\"On\"")
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "${commands[@]}" --cmake-flags "${cmakeflags[@]}" --template $template -d
}

build_tn93()
{
    name=tn93
    url=https://github.com/veg/tn93/archive/v1.0.6.tar.gz
    version=1.0.6
    commands="tn93 -h 2>&1 | grep 'usage'"
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "$commands" --template $template
}

build_lambda()
{
    name=lambda2
    url=https://github.com/seqan/lambda/archive/lambda-v2.0.0.tar.gz
    version=2.0.0
    commands="lambda2 --help"
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "$commands" --template $template
}

build_newick_utils()
{
    name=newick-utils
    url=https://github.com/tjunier/newick_utils/archive/da121155a977197cab9fbb15953ca1b40b11eb87.tar.gz
    version=1.6
    commands=("nw_clade -h" "nw_condense -h" "nw_distance -h" "nw_duration -h" "nw_ed -h" "nw_gen -h" "nw_indent -h" "nw_labels -h" "nw_match -h" "nw_order -h" "nw_prune -h" "nw_rename -h" "nw_reroot -h" "nw_stats -h" "nw_support -h" "nw_topology -h" "nw_trim -h" "nw_display -h")
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "${commands[@]}" --template $template
}

build_netreg()
{
    name=netreg
    url=https://github.com/dirmeier/netReg/archive/v1.8.0.tar.gz
    version=1.8.0
    commands="netReg -h"
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "$commands" --template $template
}

build_simka()
{
    name=simka
    url=https://github.com/GATB/simka/releases/download/v1.5.1/simka-v1.5.1-Source.tar.gz
    version=1.5.1
    commands=("simka -h" "simkaMin.py --help")
    template="cmake"
    bioconda-recipe-gen $BR_PATH -n $name -u $url -v $version --test-commands "${commands[@]}" --template $template
}

build_2pg_cartesian()
{
    name=2pg_cartesian
    url=https://github.com/rodrigofaccioli/2pg_cartesian/archive/v1.0.1.tar.gz
    version=1.0.1
    commands="protpred-Gromacs-Test_random_number"
    pfiles=$DATA_PATH/2pg_cartesian
    template="cmake"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --test-commands "$commands" --patches $pfiles --template $template
}

build_nanomath()
{
    name=nanomath
    url=https://pypi.io/packages/source/n/nanomath/nanomath-0.23.1.tar.gz
    version=0.23.1
    command_imports="nanomath"
    template="python"
    bioconda-recipe-gen $BR_PATH from-args -n $name -u $url -v $version --imports "$command_imports"  --template $template
}

build_fuma()
{
    data=$DATA_PATH/fuma
    yes | bioconda-recipe-gen $BR_PATH from-files $data --strategy python2
}

build_crossmap()
{
    data=$DATA_PATH/crossmap
    yes | bioconda-recipe-gen $BR_PATH from-files $data --strategy python3 -d
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
    netreg)		        build_netreg;;
    lambda)             build_lambda;;
    newick-utils)       build_newick_utils;;
    simka)              build_simka;;
    denovogear)         build_denovogear;;
    2pg-cartesian)      build_2pg_cartesian;;
    nanomath)           build_nanomath;;
    fuma)               build_fuma;;
    crossmap)           build_crossmap;;
esac
