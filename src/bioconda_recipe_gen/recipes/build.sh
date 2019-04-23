#!/bin/bash
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$PREFIX ..
make
make install

