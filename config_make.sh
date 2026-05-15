#!/bin/bash

export LDSHARED_FLAGS=" -bundle -undefined dynamic_lookup"
export PREFIX=$(python -c "import sys; print(sys.prefix)")
./configure --prefix=$PREFIX \
            --with-python \
            --with-uuid=$PREFIX \
            --with-json-c=$PREFIX \
            --with-udunits2=$PREFIX \
            --with-netcdf=$PREFIX \
            --enable-verbose-test
make distclean
make install
