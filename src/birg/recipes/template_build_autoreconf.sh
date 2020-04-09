autoreconf -fi
./configure --prefix=$PREFIX
make
make install
