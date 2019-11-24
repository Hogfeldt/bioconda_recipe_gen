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
    # TODO: Consider how to handle the string below wich is a substring of another string adding make to build
    #    'cmake was unable to find a build program corresponding to "unix makefiles"': (
    #        "make",
    #        "host",
    #    ),  # CMake Error: CMake was unable to find a build program corresponding to "Unix Makefiles".  CMAKE_MAKE_PROGRAM is not set.  You probably need to select a different build tool.
    'cmake was unable to find a build program corresponding to "unix makefiles"': (
        "make",
        "host",
    ),  # CMake Error: CMake was unable to find a build program corresponding to "Unix Makefiles".  CMAKE_MAKE_PROGRAM is not set.  You probably need to select a different build tool.
    'could not find a package configuration file provided by "bpp-seq"': (
        "bpp-seq",
        "build",
    ),  # Could not find a package configuration file provided by "bpp-seq" (requested version 12.0.0) with any of the following names:
    "configure: error: zlib development files not found": (
        "zlib",
        "host",
    ),  # configure: error: zlib development files not found
    "configure: error: libbzip2 development files not found": (
        "bzip2",
        "host",
    ),  # configure: error: libbzip2 development files not found
    "configure: error: liblzma development files not found": (
        "xz",
        "host",
    ),  # configure: error: liblzma development files not found
    "configure: error: libcurl library not found": (
        "curl",
        "host",
    ),  # configure: error: libcurl library not found
    "./autogen.sh: autoconf: not found": (
        "autoconf",
        "build",
    ),  # ./autogen.sh: 5: ./autogen.sh: autoconf: not found
    "jemalloc version   : 0.0.0": (
        "jemalloc  >=5.1.0",
        "host",
    ),  # jemalloc version   : 0.0.0-0-g0000000000000000000000000000000000000000
    'could not find a package configuration file provided by "bpp-core"': (
        "bpp-core",
        "build",
    ),  # Could not find a package configuration file provided by "bpp-core" (requested version 4.0.0) with any of the following names:
    "required library htslib not found": (
        "htslib",
        "host",
    ),  # Could not find a package configuration file provided by "bpp-core" (requested version 4.0.0) with any of the following names:
    "eigen3 library not found": (
        "eigen",
        "host",
    ),  # Eigen3 library not found.  Either install it or rerun cmake with
    "could not find eigen3": (
        "eigen",
        "host",
    ),  # Could NOT find Eigen3 (missing: EIGEN3_INCLUDE_DIR EIGEN3_VERSION_OK) (Required is at least version "2.91.0")
    "meson.build:1:0: error: unknown compiler(s): ['c++', 'g++', 'clang++', 'pgc++', 'icpc']": (
        "{{ compiler('cxx') }}",
        "build",
    ),
    "fatal error: api/bamreader.h: no such file or directory": (
        "bamtools",
        "build",
    ),  # /opt/conda/conda-bld/transrate-tools_1574079281000/work/src/bam-read.h:6:10: fatal error: api/BamReader.h: No such file or directory
    "make: wall: command not found": (
        "{{ compiler('cxx') }}",
        "build",
    ),

    ##############################################
    ################### PYTHON ###################
    ##############################################
    "be sure to add all dependencies in the meta.yaml  url=https://pypi.org/simple/twine/": (
        "twine",
        "host",
    ),  # RuntimeError: Setuptools downloading is disabled in conda build. Be sure to add all dependencies in the meta.yaml  url=https://pypi.org/simple/twine/
    "modulenotfounderror: no module named 'click'": (
        "click",
        "run",
    ),
    "importerror: no module named cookiecutter.main": (
        "cookiecutter",
        "run",
    ),  # import cookiecutter.main, cookiecutter.exceptions ImportError: No module named cookiecutter.main
    "modulenotfounderror: no module named 'git'": (
        "gitpython",
        "run",
    ),
    "modulenotfounderror: no module named 'tabulate'": (
        "tabulate",
        "run",
    ),
    #"importerror: no module named git": (
    #    "git",
    #    "run",
    #),
}
