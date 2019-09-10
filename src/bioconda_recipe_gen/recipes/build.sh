#!/bin/bash

mkdir -p build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$PREFIX -DBUILD_DIVSUFSORT64="On" 
make
make install
