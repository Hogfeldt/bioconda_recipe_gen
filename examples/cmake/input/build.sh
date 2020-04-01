#!/bin/bash
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBOOST_ROOT="${PREFIX}" -DCMAKE_CXX_COMPILER="${CXX}" ..
make
make install