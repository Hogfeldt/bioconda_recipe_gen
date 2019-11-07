str_to_pkg = {
    "autoheader: not found": ("autoconf", "build"),
    "autoreconf: command not found": ("automake", "build"),
    "autoreconf: failed to run aclocal": ("automake", "build"),
    "could not find hdf5": ("hdf5", "host"),
    "unable to find the requested boost libraries": ("boost", "host"),
    "could not find boost": ("boost", "host"),
    "no cmake_cxx_compiler could be found": ("{{ compiler('cxx') }}", "build"),
    'could not find a package configuration file provided by "seqan"': (
        "seqan-library",
        "build",
    ),
    "could not find bison": ("bison", "build"),
    "bison: command not found": ("bison", "build"),
    "could not find flex": ("flex", "build"),
    "flex: command not found": ("flex", "build"),
    "could not find libxml2": ("libxml2", "build"),
    "could not find armadillo": ("armadillo", "host"),
    "error: libtool library used but": ("libtool", "build"),
    "could not find blas (missing: blas_libraries)": ("openblas", "host"),
    "['zlib'] not in reqs/run": ("zlib", "run"),
    "fatal error: zlib.h: no such file or directory": ("zlib", "host"),
    "fatal error: boost": (
        "boost",
        "host",
    ),  # /opt/conda/conda-bld/lorma_1572881017031/work/thirdparty/gatb-core/src/gatb/tools/designpattern/impl/IteratorHelpers.hpp:32:10: fatal error: boost/variant.hpp: No such file or directory
    'cmake error: cmake was unable to find a build program corresponding to "unix makefiles"': (
        "make",
        "build",
    ),
    "could not find gsl (missing: gsl_libraries)": ("gsl", "host"),
    "fatal error: nlopt.h: no such file or directory": ("nlopt", "host"),
    "make: command not found": ("make", "build"),
    "meson: command not found": ("meson", "build"),
    "fatal error: curl/curl.h: no such file or directory": (
        "curl",
        "host",
    ),  # /opt/conda/conda-bld/hyphy_1573135156244/work/src/utils/hyphyunixutils.cpp:44:14: fatal error: curl/curl.h: No such file or directory
    'cmake was unable to find a build program corresponding to "unix makefiles"': (
        "make",
        "host",
    ),  # CMake Error: CMake was unable to find a build program corresponding to "Unix Makefiles".  CMAKE_MAKE_PROGRAM is not set.  You probably need to select a different build tool.
}
